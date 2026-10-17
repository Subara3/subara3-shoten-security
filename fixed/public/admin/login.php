<?php require __DIR__ . '/../../app/config.php';
$err = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $login = (string)($_POST['login'] ?? '');
    $pass  = (string)($_POST['password'] ?? '');
    $ip    = (string)($_SERVER['REMOTE_ADDR'] ?? '');

    // ログイン試行のロックアウト：同じ接続元が15分で10回失敗したら、しばらく受け付けない
    $rc = mysqli_prepare(db(), 'SELECT COUNT(*) AS n FROM admin_login_log WHERE ip=? AND success=0 AND at > (NOW() - INTERVAL 15 MINUTE)');
    mysqli_stmt_bind_param($rc, 's', $ip);
    mysqli_stmt_execute($rc);
    $locked = (int)(mysqli_fetch_assoc(mysqli_stmt_get_result($rc))['n'] ?? 0) >= 10;

    $ok = 0;
    if (!$locked) {
        $st = mysqli_prepare(db(), 'SELECT * FROM admins WHERE login=? AND active=1');
        mysqli_stmt_bind_param($st, 's', $login);
        mysqli_stmt_execute($st);
        $row = mysqli_fetch_assoc(mysqli_stmt_get_result($st));
        if ($row) {
            if (password_verify($pass, $row['password'])) {
                $ok = 1;
            } elseif (strlen($row['password']) === 32 && hash_equals($row['password'], md5($pass))) {
                // 旧形式（塩なしMD5）のまま残っている人は、ログインできた時点で作り直す
                $ok = 1;
                $new = password_hash($pass, PASSWORD_DEFAULT);
                $up = mysqli_prepare(db(), 'UPDATE admins SET password=? WHERE id=?');
                mysqli_stmt_bind_param($up, 'si', $new, $row['id']);
                mysqli_stmt_execute($up);
            }
        }
    }

    // 試行は成否にかかわらず記録する（止めた試行も success=0 として残る）
    $log = mysqli_prepare(db(), 'INSERT INTO admin_login_log (login, ip, success, at) VALUES (?, ?, ?, NOW())');
    mysqli_stmt_bind_param($log, 'ssi', $login, $ip, $ok);
    mysqli_stmt_execute($log);

    if ($locked) {
        $err = 'ログイン試行が続いたため、しばらく受け付けません。時間をおいてから試してください。';
    } elseif ($ok) {
        session_regenerate_id(true);
        $_SESSION['admin'] = ['id' => $row['id'], 'login' => $row['login'], 'role' => $row['role']];
        mysqli_query(db(), 'UPDATE admins SET last_login=NOW() WHERE id=' . (int)$row['id']);
        header('Location: index.php'); exit;
    } else {
        $err = 'ログインできません';
    }
}
?><!doctype html><meta charset="utf-8"><title>管理画面</title>
<h1>すばら３商店 管理画面</h1><p><?= h($err) ?></p>
<form method="post"><input name="login"><input name="password" type="password"><button>ログイン</button></form>
