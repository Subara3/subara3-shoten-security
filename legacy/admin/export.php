<?php require 'auth.php';
// 全会員をCSVで出す（退会者も含む）
header('Content-Type: text/csv; charset=UTF-8');
header('Content-Disposition: attachment; filename="members.csv"');
$res = mysqli_query(db(), 'SELECT email,name,zip,address,tel,birthday,status FROM members');
$out = fopen('php://output', 'w');
while ($m = mysqli_fetch_row($res)) fputcsv($out, $m);
