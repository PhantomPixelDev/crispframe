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
echo sprintf("Static syntax passed: %d YAML, %d XML/XLIFF, %d PHP files.\n", ...array_values($counts));
