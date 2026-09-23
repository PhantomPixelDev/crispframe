<?php
declare(strict_types=1);

$path = parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH) ?: '/';
$public = $_SERVER['DOCUMENT_ROOT'];
$file = realpath($public . $path);
if ($file !== false && str_starts_with($file, $public . DIRECTORY_SEPARATOR) && is_file($file)) {
    return false;
}
require $public . '/index.php';
