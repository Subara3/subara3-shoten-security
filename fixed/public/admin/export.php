<?php require 'auth.php';
// 会員CSVは店長（owner）だけ。退会者は出さない。誰がいつ出したかを残す
if ($_SESSION['admin']['role'] !== 'owner') { http_response_code(403); exit('権限がありません'); }
$res = mysqli_query(db(), "SELECT email,name,zip,address,tel FROM members WHERE status='active'");
audit($_SESSION['admin']['login'], 'export_members', mysqli_num_rows($res) . ' rows');
header('Content-Type: text/csv; charset=UTF-8');
header('Content-Disposition: attachment; filename="members.csv"');
$out = fopen('php://output', 'w');
while ($m = mysqli_fetch_row($res)) fputcsv($out, $m);
