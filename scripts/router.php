<?php
declare(strict_types=1);

$path = rawurldecode(parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH) ?: '/');
$public = $_SERVER['DOCUMENT_ROOT'];
// Composer publishes assets through symlinks outside public/. The built-in
// server can serve them directly, provided the URL path itself has no traversal.
if (!str_contains($path, '..') && is_file($public . $path)) {
    return false;
}
require $public . '/index.php';
