<?php
/* Sidhu Legal — website lead intake handler.
 * UPLOAD to each domain ROOT (e.g. injury-lawyer-calgary.com/mail.php,
 * injury-lawyer-edmonton.com/mail.php, sidhulegal.com/mail.php).
 * The contact forms POST here; it emails the lead to $to.
 * Forms send: name, phone, case_type, message (email is optional). */

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    exit;
}

header('Content-Type: application/json');

$to = 'info@ngsidhu.com';   // <-- where leads are emailed (change if needed)

// Honeypot: bots fill hidden fields -> drop silently
if (!empty($_POST['company']) || !empty($_POST['website'])) {
    echo json_encode(['ok' => true]);
    exit;
}

$name    = strip_tags(trim($_POST['name'] ?? ''));
$phone   = strip_tags(trim($_POST['phone'] ?? ''));
$email   = filter_var(trim($_POST['email'] ?? ''), FILTER_SANITIZE_EMAIL);
$matter  = strip_tags(trim($_POST['case_type'] ?? ($_POST['matter'] ?? '')));
$message = strip_tags(trim($_POST['message'] ?? ''));
$page    = strip_tags(trim($_POST['page'] ?? ($_SERVER['HTTP_REFERER'] ?? '')));

// Require name + phone (forms don't collect email)
if (!$name || !$phone) {
    http_response_code(422);
    echo json_encode(['ok' => false, 'error' => 'Name and phone are required.']);
    exit;
}

$nl = function ($s) { return preg_replace('/[\r\n]+/', ' ', $s); }; // header-injection guard

$subject = 'New Case Review — ' . $nl($name);

$body  = "New lead from your website:\n\n";
$body .= "Name:    $name\n";
$body .= "Phone:   $phone\n";
if ($email !== '')   { $body .= "Email:   $email\n"; }
if ($matter !== '')  { $body .= "Case:    $matter\n"; }
if ($message !== '') { $body .= "Message: $message\n"; }
$body .= "Page:    $page\n";
$body .= "Time:    " . date('Y-m-d H:i:s T') . "\n";
$body .= "IP:      " . ($_SERVER['REMOTE_ADDR'] ?? '') . "\n";

$headers  = "From: noreply@" . ($_SERVER['HTTP_HOST'] ?? 'sidhulegal.com') . "\r\n";
if ($email !== '' && filter_var($email, FILTER_VALIDATE_EMAIL)) {
    $headers .= "Reply-To: $email\r\n";
}
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

$envelope = '-fnoreply@' . ($_SERVER['HTTP_HOST'] ?? 'sidhulegal.com');
echo json_encode(['ok' => (bool) @mail($to, $nl($subject), $body, $headers, $envelope)]);
