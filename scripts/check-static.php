<?php
declare(strict_types=1);

require dirname(__DIR__) . '/vendor/autoload.php';

use Symfony\Component\Yaml\Yaml;

$root = dirname(__DIR__);
$paths = [
    $root . '/packages/agency_theme',
    $root . '/packages/agency_demo',
    $root . '/starter',
    $root . '/config',
    $root . '/.github',
];
$counts = ['yaml' => 0, 'xml' => 0, 'php' => 0];
foreach ($paths as $path) {
    $files = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($path, FilesystemIterator::SKIP_DOTS));
    foreach ($files as $file) {
        $name = $file->getPathname();
        $extension = strtolower($file->getExtension());
        if (in_array($extension, ['yaml', 'yml'], true) || str_ends_with($name, '.yaml.example')) {
            Yaml::parseFile($name);
            $counts['yaml']++;
        } elseif (in_array($extension, ['xlf', 'xml'], true)) {
            $document = new DOMDocument();
            if (!$document->load($name, LIBXML_NONET)) {
                throw new RuntimeException("Invalid XML: $name");
            }
            $counts['xml']++;
        } elseif ($extension === 'php') {
            $command = escapeshellarg(PHP_BINARY) . ' -l ' . escapeshellarg($name);
            exec($command, $output, $exitCode);
            if ($exitCode !== 0) {
                throw new RuntimeException("Invalid PHP: $name\n" . implode("\n", $output));
            }
            $counts['php']++;
        }
    }
}
$sprite = file_get_contents($root . '/packages/agency_theme/Resources/Public/Icons/sprite.svg');
preg_match_all('/id="icon-([^"]+)"/', $sprite, $matches);
$symbols = array_fill_keys($matches[1], true);
$legacy = ['strategy', 'design', 'code', 'star', 'check', 'arrow-right'];
foreach (['services', 'feature-grid'] as $block) {
    $base = $root . '/packages/agency_theme/ContentBlocks/ContentElements/' . $block;
    $config = Yaml::parseFile($base . '/config.yaml');
    $collection = array_values(array_filter($config['fields'], static fn(array $field): bool => $field['identifier'] === 'items'))[0];
    $icon = array_values(array_filter($collection['fields'], static fn(array $field): bool => $field['identifier'] === 'icon'))[0];
    $choices = array_column($icon['items'], 'value');
    foreach ($legacy as $name) {
        if (!in_array($name, $choices, true)) {
            throw new RuntimeException("Missing legacy icon $name in $block");
        }
    }
    foreach ($choices as $name) {
        if ($name !== 'none' && !isset($symbols[$name])) {
            throw new RuntimeException("Missing sprite symbol icon-$name in $block");
        }
        foreach (['labels.xlf', 'de.labels.xlf'] as $catalog) {
            if (!str_contains(file_get_contents($base . '/language/' . $catalog), 'items.icon.items.' . $name . '.label')) {
                throw new RuntimeException("Missing $name editor label in $block/$catalog");
            }
        }
    }
}
echo sprintf("Static syntax passed: %d YAML, %d XML/XLIFF, %d PHP files.\n", ...array_values($counts));
