<?php require_once __DIR__ . '/../../app/config.php';
if (empty($_SESSION['admin'])) { header('Location: login.php'); exit; }
