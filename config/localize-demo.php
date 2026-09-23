<?php
declare(strict_types=1);

// Development helper: create connected German translations for demo pages.
$loader = require dirname(__DIR__) . '/vendor/autoload.php';
\TYPO3\CMS\Core\Core\SystemEnvironmentBuilder::run(0, \TYPO3\CMS\Core\Core\SystemEnvironmentBuilder::REQUESTTYPE_CLI);
\TYPO3\CMS\Core\Core\Bootstrap::init($loader);
\TYPO3\CMS\Core\Core\Bootstrap::initializeBackendUser(\TYPO3\CMS\Core\Authentication\CommandLineUserAuthentication::class);
\TYPO3\CMS\Core\Core\Bootstrap::initializeBackendAuthentication();
$GLOBALS['LANG'] = \TYPO3\CMS\Core\Utility\GeneralUtility::makeInstance(\TYPO3\CMS\Core\Localization\LanguageServiceFactory::class)->createFromUserPreferences($GLOBALS['BE_USER']);

$pool = \TYPO3\CMS\Core\Utility\GeneralUtility::makeInstance(\TYPO3\CMS\Core\Database\ConnectionPool::class);
$pages = $pool->getConnectionForTable('pages');
$content = $pool->getConnectionForTable('tt_content');
$cmd = ['pages' => [], 'tt_content' => []];
foreach ($pages->fetchAllAssociative('SELECT uid FROM pages WHERE uid = 1 OR (pid = 1 AND deleted = 0 AND sys_language_uid = 0)') as $page) {
    $uid = (int)$page['uid'];
    if (!$pages->fetchOne('SELECT uid FROM pages WHERE l10n_parent = ? AND sys_language_uid = 1 AND deleted = 0', [$uid])) {
        $cmd['pages'][$uid] = ['localize' => 1];
    }
}
foreach ($content->fetchAllAssociative('SELECT uid FROM tt_content WHERE deleted = 0 AND sys_language_uid = 0') as $record) {
    $uid = (int)$record['uid'];
    if (!$content->fetchOne('SELECT uid FROM tt_content WHERE l18n_parent = ? AND sys_language_uid = 1 AND deleted = 0', [$uid])) {
        $cmd['tt_content'][$uid] = ['localize' => 1];
    }
}
$handler = \TYPO3\CMS\Core\Utility\GeneralUtility::makeInstance(\TYPO3\CMS\Core\DataHandling\DataHandler::class);
$handler->start([], $cmd);
$handler->process_cmdmap();
if ($handler->errorLog) {
    throw new RuntimeException(implode("\n", $handler->errorLog));
}

$pageCopy = [
    1 => ['title' => 'Startseite', 'slug' => '/'],
    2 => ['title' => 'Projekte', 'slug' => '/work'],
    3 => ['title' => 'Kontakt', 'slug' => '/contact'],
    4 => ['title' => 'Komponenten', 'slug' => '/components'],
];
foreach ($pageCopy as $original => $fields) {
    $pages->update('pages', $fields + ['hidden' => 0, 'nav_title' => $fields['title']], ['l10n_parent' => $original, 'sys_language_uid' => 1]);
}

$copy = [
    'Demo: home hero' => ['crispframe_hero_eyebrow' => 'Strategie · Design · Entwicklung', 'crispframe_hero_headline' => 'Digitale Erlebnisse mit Klarheit gestalten', 'crispframe_hero_subheadline' => 'Wir machen komplexe Ideen zu zugänglichen Websites und digitalen Produkten.', 'crispframe_hero_primaryLinkLabel' => 'Projekt anfragen', 'crispframe_hero_secondaryLinkLabel' => 'Projekte ansehen'],
    'Demo: approach' => ['crispframe_intro_headline' => 'Gute Arbeit beginnt mit Verstehen', 'crispframe_intro_lead' => 'Ein Team für den gesamten Weg.', 'crispframe_intro_text' => 'Wir verbinden Recherche, Design und Umsetzung, damit jede Entscheidung Ihren Kunden und Ihrem Unternehmen dient.', 'crispframe_intro_linkLabel' => 'Mehr erfahren'],
    'Demo: services' => ['crispframe_services_headline' => 'Was wir gemeinsam entwickeln können', 'crispframe_services_lead' => 'Ein flexibler Ausgangspunkt für Ihr eigenes Leistungsangebot.'],
    'Demo: features' => ['crispframe_featuregrid_headline' => 'Für alle, die mit der Website arbeiten', 'crispframe_featuregrid_lead' => 'Eine gute Plattform unterstützt Besucher und Redaktion gleichermaßen.'],
    'Demo: home CTA' => ['crispframe_cta_headline' => 'Eine Herausforderung, die wir lösen können?', 'crispframe_cta_text' => 'Erzählen Sie uns von Ihrem Vorhaben. Gemeinsam finden wir den nächsten Schritt.', 'crispframe_cta_primaryLinkLabel' => 'Kontakt aufnehmen'],
    'Demo: work hero' => ['crispframe_hero_eyebrow' => 'Ausgewählte Arbeiten', 'crispframe_hero_headline' => 'Arbeit mit Wirkung', 'crispframe_hero_subheadline' => 'Klare Ideen und sorgfältige Umsetzung für langlebige digitale Erlebnisse.'],
    'Demo: work intro' => ['crispframe_intro_headline' => 'Projekte mit echten Anforderungen', 'crispframe_intro_lead' => 'Von der ersten Frage bis zum zuverlässigen Start.', 'crispframe_intro_text' => 'Unsere Projekte verbinden Inhalt, Interaktion und Technik. Ergänzen Sie hier Ihre eigenen Fallstudien.'],
    'Demo: project examples' => ['crispframe_projects_headline' => 'Beispielprojekte', 'crispframe_projects_lead' => 'Ersetzen Sie diese Beispiele durch Ihre eigenen Referenzen.'],
    'Demo: contact hero' => ['crispframe_hero_eyebrow' => 'Kontakt', 'crispframe_hero_headline' => 'Lassen Sie uns sprechen', 'crispframe_hero_subheadline' => 'Wir freuen uns, von Ihrem Vorhaben zu hören.'],
    'Demo: contact details' => ['crispframe_contact_headline' => 'Kontakt aufnehmen', 'crispframe_contact_lead' => 'Teilen Sie Ihre Idee, Anfrage oder Frage mit uns.', 'crispframe_contact_note' => 'Beispieldaten: Ersetzen Sie diese Angaben vor der Veröffentlichung.'],
    'Demo: pricing' => ['crispframe_pricing_headline' => 'Flexible Zusammenarbeit', 'crispframe_pricing_lead' => 'Beispielangebote. Ersetzen Sie Preise und Leistungen durch Ihr eigenes Angebot.', 'crispframe_pricing_monthlySuffix' => '/ Monat', 'crispframe_pricing_yearlySuffix' => '/ Monat, jährlich abgerechnet', 'crispframe_pricing_footnote' => 'Beispielpreise; Leistungsumfang und Steuern hängen von der Vereinbarung ab.'],
    'Demo: privacy-friendly video' => ['crispframe_video_headline' => 'Ein Video, das auf Ihren Klick wartet', 'crispframe_video_lead' => 'Der Videoanbieter wird erst nach dem Klick auf Play kontaktiert.', 'crispframe_video_caption' => 'Beispielvideo. Ersetzen Sie ID, Vorschaubild und Transkript.', 'crispframe_video_transcript' => 'Dies ist ein Beispielblock. Ergänzen Sie für Ihr eigenes Video ein vollständiges Transkript.'],
    'Demo: gallery' => ['crispframe_gallery_headline' => 'Eine Galerie für Projektbilder', 'crispframe_gallery_lead' => 'Jedes Bild kann eine eigene Beschriftung und einen alternativen Text haben.'],
    'Demo: text and image' => ['crispframe_textimage_headline' => 'Inhalte mit Raum zum Wirken', 'crispframe_textimage_lead' => 'Ein flexibles redaktionelles Layout.', 'crispframe_textimage_text' => 'Kombinieren Sie einen kurzen Text mit einem Bild oder lassen Sie das Bild weg, wenn die Worte für sich stehen.'],
    'Demo: statistics' => ['crispframe_stats_headline' => 'Zahlen mit klarer Bedeutung', 'crispframe_stats_lead' => 'Ersetzen Sie Beispielwerte durch geprüfte Ergebnisse.'],
    'Demo: logo cloud' => ['crispframe_logocloud_headline' => 'Partner und Mitwirkende', 'crispframe_logocloud_lead' => 'Verwenden Sie Logos nur mit Erlaubnis.'],
    'Demo: testimonials' => ['crispframe_testimonials_headline' => 'So kann Zusammenarbeit aussehen', 'crispframe_testimonials_lead' => 'Ersetzen Sie diese erfundenen Zitate durch freigegebene Kundenstimmen.'],
    'Demo: team' => ['crispframe_team_headline' => 'Menschen hinter der Arbeit', 'crispframe_team_lead' => 'Stellen Sie echte Personen mit deren Zustimmung vor.'],
    'Demo: process' => ['crispframe_process_headline' => 'Ein klarer Weg von der Idee zum Start', 'crispframe_process_lead' => 'Zeigen Sie Besuchern einfach, was als Nächstes passiert.'],
    'Demo: frequently asked questions' => ['crispframe_faq_headline' => 'Häufige Fragen', 'crispframe_faq_lead' => 'Antworten Sie kurz und konkret.'],
];
foreach ($copy as $marker => $fields) {
    $original = $content->fetchOne('SELECT uid FROM tt_content WHERE header = ? AND sys_language_uid = 0 AND deleted = 0', [$marker]);
    if ($original) {
        $content->update('tt_content', $fields + ['hidden' => 0, 'header' => $marker], ['l18n_parent' => (int)$original, 'sys_language_uid' => 1]);
    }
}
// The form element has no translated editorial text, but must be enabled.
$content->executeStatement('UPDATE tt_content SET hidden = 0 WHERE sys_language_uid = 1 AND deleted = 0');

$childCopy = [
    'crispframe_services_items' => [
        ['title' => 'Strategie', 'description' => 'Geschäftsziele und Nutzerbedürfnisse in einen klaren digitalen Plan übersetzen.', 'linkLabel' => 'Projekt besprechen'],
        ['title' => 'Design', 'description' => 'Verständliche Oberflächen und eine passende visuelle Sprache gestalten.', 'linkLabel' => 'Projekt besprechen'],
        ['title' => 'Entwicklung', 'description' => 'Wartbare TYPO3-Websites und digitale Erlebnisse entwickeln.', 'linkLabel' => 'Projekt besprechen'],
    ],
    'crispframe_featuregrid_items' => [
        ['title' => 'Barrierearm gestaltet', 'description' => 'Lesbare Inhalte, klare Navigation und Bedienung per Tastatur.'],
        ['title' => 'Einfach zu pflegen', 'description' => 'Strukturierte Bausteine erleichtern tägliche Änderungen ohne Neuentwicklung.'],
        ['title' => 'Bereit für Neues', 'description' => 'Wiederverwendbare Seitenmuster lassen Raum für neue Inhalte und Leistungen.'],
    ],
    'crispframe_projects_items' => [
        ['title' => 'Unternehmenswebsite', 'category' => 'Beispiel', 'description' => 'Eine klare Darstellung von Leistungen, Menschen und Fachwissen.'],
        ['title' => 'Kundenportal', 'category' => 'Beispiel', 'description' => 'Ein übersichtlicher Arbeitsbereich für wiederkehrende Aufgaben.'],
        ['title' => 'Redaktionsplattform', 'category' => 'Beispiel', 'description' => 'Flexible Veröffentlichung für verteilte Teams.'],
    ],
    'crispframe_pricing_tiers' => [
        ['name' => 'Basis', 'summary' => 'Ein guter Start für fokussierte Teams.', 'features' => '<ul><li>Inhalts- und Designprüfung</li><li>Monatlicher Verbesserungsplan</li><li>Support per E-Mail</li></ul>', 'ctaLabel' => 'Basis anfragen'],
        ['name' => 'Wachstum', 'summary' => 'Laufendes Design und Entwicklung.', 'features' => '<ul><li>Kontinuierliche TYPO3-Verbesserungen</li><li>Bevorzugter Support</li><li>Monatliche Strategiesitzung</li></ul>', 'ctaLabel' => 'Wachstum besprechen'],
        ['name' => 'Partnerschaft', 'summary' => 'Ein festes Team für anspruchsvolle Projekte.', 'monthlyPrice' => 'Auf Anfrage', 'yearlyPrice' => 'Auf Anfrage', 'features' => '<ul><li>Festes Umsetzungsteam</li><li>Produktplanung</li><li>Individuelle Vereinbarung</li></ul>', 'ctaLabel' => 'Partnerschaft planen'],
    ],
    'crispframe_gallery_items' => [
        ['caption' => 'Ein klarer Arbeitsbereich'],
        ['caption' => 'Ideen in Bewegung'],
    ],
    'crispframe_stats_items' => [
        ['label' => 'Beispielstarts'],
        ['label' => 'Jahre Zusammenarbeit'],
        ['label' => 'Fachbereiche'],
    ],
    'crispframe_logocloud_items' => [
        ['name' => 'Beispielpartner eins'],
        ['name' => 'Beispielpartner zwei'],
        ['name' => 'Beispielpartner drei'],
    ],
    'crispframe_testimonials_items' => [
        ['quote' => 'Das Team hat eine komplexe Aufgabe übersichtlich gemacht.', 'author' => 'Beispielperson', 'role' => 'Beispielorganisation'],
    ],
    'crispframe_team_items' => [
        ['name' => 'Alex Beispiel', 'role' => 'Designleitung', 'bio' => 'Gestaltet klare Oberflächen und Inhaltssysteme.'],
        ['name' => 'Sam Beispiel', 'role' => 'Technische Leitung', 'bio' => 'Entwickelt wartbare Veröffentlichungslösungen.'],
    ],
    'crispframe_process_items' => [
        ['title' => 'Verstehen', 'description' => 'Ziele, Zielgruppen und Rahmenbedingungen klären.'],
        ['title' => 'Gestalten', 'description' => 'Die passende Lösung entwerfen und umsetzen.'],
        ['title' => 'Verbessern', 'description' => 'Aus der Nutzung lernen und weiterentwickeln.'],
    ],
    'crispframe_faq_items' => [
        ['question' => 'Kann ich Inhalte selbst ändern?', 'answer' => 'Ja. Jeder Abschnitt ist ein bearbeitbares TYPO3-Inhaltselement.'],
        ['question' => 'Kann ich eine andere Farbpalette nutzen?', 'answer' => 'Ja. Wählen Sie eine Palette in den Site Settings.'],
    ],
];
foreach ($childCopy as $table => $items) {
    $connection = $pool->getConnectionForTable($table);
    $rows = $connection->fetchAllAssociative('SELECT uid FROM ' . $table . ' WHERE sys_language_uid = 1 AND deleted = 0 ORDER BY uid');
    foreach ($rows as $index => $row) {
        if (isset($items[$index])) {
            $connection->update($table, $items[$index], ['uid' => (int)$row['uid']]);
        }
    }
}
echo "German demo records localized and translated.\n";
