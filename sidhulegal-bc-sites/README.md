# Sidhu Legal — BC Personal Injury Landing Pages

Static, single-page landing sites for **Sidhu Legal** (NG Sidhu Law) personal injury / ICBC
practice, targeting 10 cities across BC's Lower Mainland & Fraser Valley. One office in
Surrey serving the region.

## Sites

| Folder | Live URL (on deploy) |
|---|---|
| `sidhulegal-surrey` | sidhulegal.com/surrey-personal-injury-lawyer/ |
| `sidhulegal-abbotsford` | sidhulegal.com/abbotsford-personal-injury-lawyer/ |
| `sidhulegal-burnaby` | sidhulegal.com/burnaby-personal-injury-lawyer/ |
| `sidhulegal-coquitlam` | sidhulegal.com/coquitlam-personal-injury-lawyer/ |
| `sidhulegal-delta` | sidhulegal.com/delta-personal-injury-lawyer/ |
| `sidhulegal-langley` | sidhulegal.com/langley-personal-injury-lawyer/ |
| `sidhulegal-mapleridge` | sidhulegal.com/maple-ridge-personal-injury-lawyer/ |
| `sidhulegal-newwestminster` | sidhulegal.com/new-westminster-personal-injury-lawyer/ |
| `sidhulegal-richmond` | sidhulegal.com/richmond-personal-injury-lawyer/ |
| `sidhulegal-vancouver` | sidhulegal.com/vancouver-personal-injury-lawyer/ |

Each folder is self-contained: `index.html`, `thank-you.html`, `privacy-policy.html`,
`404.html`, `favicon.svg`, `llms.txt`, and `mail.php` (lead intake handler).

## Features

- **6-language UI** (EN / FR / PA / HI / ZH / ES) via client-side switcher. Translations cover
  hero, practice areas, calculator, estimate modal, FAQ, and the thank-you page. *(Local
  Knowledge sections are translated for Surrey; the other cities are pending a future
  pre-render build.)*
- **Injury claim estimate calculator** + "Get My Real Estimate" modal.
- **Lead form** → posts to `/mail.php`, then redirects to `thank-you.html`.
- **SEO**: per-city `<title>`/meta/canonical, `LegalService` + `FAQPage` + `BreadcrumbList`
  JSON-LD (one Surrey office, per-city `areaServed`), `hreflang`, image dimensions (CLS),
  `llms.txt`, single H1, alt text throughout.
- `sidhulegal-sitemap.xml` — submit to Google Search Console after deploy.

## Deployment notes

1. Each site deploys to its city URL on `sidhulegal.com` (WordPress).
2. **`mail.php` must be uploaded to each domain/site root** — the form posts to `/mail.php`;
   lead emails only send when this PHP file is live on the host. Recipient: `info@ngsidhu.com`.
3. Upload `sidhulegal-sitemap.xml` to the site root (or submit the URLs in Search Console).
4. Verify each city's canonical slug matches its existing live page so inbound links/SEO carry over.

## Known follow-ups

- **Pre-render the language versions** to real `/pa/`, `/hi/`, etc. URLs so translated content
  is indexable (currently client-side only → only English is crawled).
- **Translate Local Knowledge** for the 9 non-Surrey cities (to be done with the pre-render).
- Add `AggregateRating` schema once real review counts are available.
