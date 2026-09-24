<?php
declare(strict_types=1);

// Regenerate editor labels for the five editorial blocks from their YAML source.
require dirname(__DIR__) . '/vendor/autoload.php';

use Symfony\Component\Yaml\Yaml;

$base = dirname(__DIR__) . '/packages/agency_theme/ContentBlocks/ContentElements';
$blocks = ['child-pages', 'tabs', 'pull-quote', 'resource-list', 'author-card'];
$german = [
    'Child page teasers' => 'Unterseiten-Teaser',
    'Show translated child pages as cards or a compact list.' => 'Übersetzte Unterseiten als Karten oder kompakte Liste anzeigen.',
    'Tabs' => 'Registerkarten',
    'Two to five panels of related content.' => 'Zwei bis fünf Bereiche mit zusammengehörigen Inhalten.',
    'Pull quote' => 'Hervorgehobenes Zitat',
    'A prominent quotation within an article or case study.' => 'Ein hervorgehobenes Zitat in einem Artikel oder Projektbericht.',
    'Resource list' => 'Ressourcenliste',
    'Curated links to pages, external sites, or files.' => 'Ausgewählte Links zu Seiten, externen Websites oder Dateien.',
    'Author card' => 'Autorenkarte',
    'A person profile for articles and case studies.' => 'Ein Personenprofil für Artikel und Projektberichte.',
    'Headline' => 'Überschrift', 'Introduction' => 'Einleitung',
    'Parent page' => 'Übergeordnete Seite',
    'Show visible direct children of this page.' => 'Sichtbare direkte Unterseiten dieser Seite anzeigen.',
    'Layout' => 'Layout', 'Cards' => 'Karten', 'Compact list' => 'Kompakte Liste',
    'Panels' => 'Bereiche', 'Tab label' => 'Beschriftung der Registerkarte',
    'Panel title' => 'Überschrift des Bereichs', 'Panel text' => 'Text des Bereichs',
    'Panel image' => 'Bild des Bereichs', 'Quotation' => 'Zitat',
    'Attribution' => 'Urheber', 'Role or organization' => 'Rolle oder Organisation',
    'Portrait' => 'Porträt', 'Resources' => 'Ressourcen',
    'Link label' => 'Linktext', 'Description' => 'Beschreibung', 'Link' => 'Link',
    'Icon' => 'Symbol', 'Arrow' => 'Pfeil', 'Guide' => 'Leitfaden',
    'Work' => 'Arbeit', 'Website' => 'Website', 'None' => 'Keines',
    'Name' => 'Name', 'Role' => 'Rolle', 'Short biography' => 'Kurzbiografie',
    'Section spacing' => 'Abschnittsabstand', 'Small' => 'Klein',
    'Default' => 'Standard', 'Large' => 'Groß',
    'Section background' => 'Abschnittshintergrund', 'Subtle' => 'Dezent',
    'Dark' => 'Dunkel', 'Brand' => 'Markenfarbe',
    'Container width' => 'Containerbreite', 'Narrow' => 'Schmal',
    'Wide' => 'Breit', 'Full' => 'Volle Breite',
];

function collect(array $fields, string $prefix = ''): array
{
    $labels = [];
    foreach ($fields as $field) {
        $id = $prefix . $field['identifier'];
        foreach (['label', 'description'] as $key) {
            if (!empty($field[$key])) {
                $labels[$id . '.' . $key] = (string)$field[$key];
            }
        }
        foreach ($field['items'] ?? [] as $item) {
            $labels[$id . '.items.' . $item['value'] . '.label'] = (string)$item['label'];
        }
        if (isset($field['fields'])) {
            $labels += collect($field['fields'], $id . '.');
        }
    }
    return $labels;
}

foreach ($blocks as $block) {
    $dir = "$base/$block";
    $config = Yaml::parseFile("$dir/config.yaml");
    $labels = ['title' => $config['title'], 'description' => $config['description']] + collect($config['fields']);
    foreach (['en' => 'labels.xlf', 'de' => 'de.labels.xlf'] as $language => $filename) {
        $document = new DOMDocument('1.0', 'UTF-8');
        $document->formatOutput = true;
        $xliff = $document->createElement('xliff');
        $xliff->setAttribute('xmlns', 'urn:oasis:names:tc:xliff:document:1.2');
        $xliff->setAttribute('version', '1.2');
        $document->appendChild($xliff);
        $file = $document->createElement('file');
        $file->setAttribute('datatype', 'plaintext');
        $file->setAttribute('original', 'labels.xlf');
        $file->setAttribute('source-language', 'en');
        $file->setAttribute('product-name', $config['name']);
        if ($language === 'de') {
            $file->setAttribute('target-language', 'de');
        }
        $xliff->appendChild($file);
        $body = $document->createElement('body');
        $file->appendChild($body);
        foreach ($labels as $id => $english) {
            $unit = $document->createElement('trans-unit');
            $unit->setAttribute('id', $id);
            $source = $document->createElement('source');
            $source->appendChild($document->createTextNode($english));
            $unit->appendChild($source);
            if ($language === 'de') {
                if (!isset($german[$english])) {
                    throw new RuntimeException("Missing German translation for: $english");
                }
                $target = $document->createElement('target');
                $target->appendChild($document->createTextNode($german[$english]));
                $unit->appendChild($target);
            }
            $body->appendChild($unit);
        }
        @mkdir("$dir/language", 0775, true);
        $document->save("$dir/language/$filename");
    }
}
echo "Generated English and German editor labels for five editorial blocks.\n";
