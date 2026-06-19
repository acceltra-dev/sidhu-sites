<?php
/* Sidhu Legal — BC website lead intake handler. Upload to each BC domain root. */
if ($_SERVER['REQUEST_METHOD'] !== 'POST') { http_response_code(405); exit; }
header('Content-Type: application/json');
$to = 'info@ngsidhu.com';
if (!empty($_POST['company']) || !empty($_POST['website'])) { echo json_encode(['ok'=>true]); exit; }
$name    = strip_tags(trim($_POST['name'] ?? ''));
$phone   = strip_tags(trim($_POST['phone'] ?? ''));
$email   = filter_var(trim($_POST['email'] ?? ''), FILTER_SANITIZE_EMAIL);
$matter  = strip_tags(trim($_POST['case_type'] ?? ($_POST['matter'] ?? '')));
$message = strip_tags(trim($_POST['message'] ?? ''));
$page    = strip_tags(trim($_POST['page'] ?? ($_SERVER['HTTP_REFERER'] ?? '')));
if (!$name || !$phone) { http_response_code(422); echo json_encode(['ok'=>false,'error'=>'Name and phone are required.']); exit; }
$nl = function ($s) { return preg_replace('/[\r\n]+/', ' ', $s); };
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
if ($email !== '' && filter_var($email, FILTER_VALIDATE_EMAIL)) { $headers .= "Reply-To: $email\r\n"; }
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
$envelope = '-fnoreply@' . ($_SERVER['HTTP_HOST'] ?? 'sidhulegal.com');
echo json_encode(['ok' => (bool) @mail($to, $nl($subject), $body, $headers, $envelope)]);
