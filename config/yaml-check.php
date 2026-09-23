<?php
require dirname(__DIR__) . '/vendor/autoload.php';
$f = $argv[1];
$y = Symfony\Component\Yaml\Yaml::parseFile($f);
echo json_encode($y, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES) . PHP_EOL;