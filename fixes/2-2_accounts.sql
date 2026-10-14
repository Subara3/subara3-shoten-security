-- IPA 2-2 / 3：アカウントの棚卸しと、作成・変更の記録

-- 管理者アカウントの作成・変更・権限変更を、アプリを通らない操作も含めて残す
CREATE TABLE IF NOT EXISTS admin_audit (
  id INT PRIMARY KEY AUTO_INCREMENT, actor VARCHAR(100), action VARCHAR(50),
  detail VARCHAR(255), ip VARCHAR(45), at DATETIME);
DROP TRIGGER IF EXISTS admins_ins;
DROP TRIGGER IF EXISTS admins_upd;
DELIMITER //
CREATE TRIGGER admins_ins AFTER INSERT ON admins FOR EACH ROW
  INSERT INTO admin_audit (actor, action, detail, at)
  VALUES (CURRENT_USER(), 'admin_created', CONCAT(NEW.login, ' role=', NEW.role), NOW());//
CREATE TRIGGER admins_upd AFTER UPDATE ON admins FOR EACH ROW
  IF NOT (OLD.role <=> NEW.role AND OLD.active <=> NEW.active AND OLD.password <=> NEW.password) THEN
    INSERT INTO admin_audit (actor, action, detail, at)
    VALUES (CURRENT_USER(), 'admin_changed',
            CONCAT(NEW.login, ' role=', OLD.role, '->', NEW.role, ' active=', OLD.active, '->', NEW.active,
                   IF(OLD.password <=> NEW.password, '', ' password changed')), NOW());
  END IF;//
DELIMITER ;

-- 使っていないアカウントを止める（消さずに止める。調査のために行は残す）
UPDATE admins SET active = 0, note = CONCAT(note, '／2026-10-14 停止：退職')          WHERE login = 'yamada';
UPDATE admins SET active = 0, note = CONCAT(note, '／2026-10-14 停止：契約終了')      WHERE login = 'arbeit01';
UPDATE admins SET active = 0, note = CONCAT(note, '／2026-10-14 停止：共用の初期アカウント') WHERE login = 'admin';
-- 制作会社が店に断らずに作っていた保守用アカウント。確認が取れたので止める
UPDATE admins SET active = 0, note = '制作会社が保守用に作成（店の承認なし）／2026-10-14 停止' WHERE login = 'support2';

SELECT login, role, active, note FROM admins ORDER BY created_at;
SELECT actor, action, detail, at FROM admin_audit ORDER BY id;
