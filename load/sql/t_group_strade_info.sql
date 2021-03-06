TRUNCATE TABLE t_group_strade_info; INSERT INTO t_group_strade_info( order_id , alipay_actual_recieve , refund , alipay_actual_recieve_usd , refund_usd , alipay_strade_p , alipay_strade_r , alipay_strade_p_usd , alipay_strade_r_usd)
SELECT TRIM('\t'
FROM order_id) , alipay_actual_recieve , refund , alipay_actual_recieve_usd , refund_usd , sum(alipay_strade_p) AS alipay_strade_p , sum(alipay_strade_r) AS alipay_strade_r , sum(alipay_strade_p_usd) AS alipay_strade_p_usd , sum(alipay_strade_r_usd) AS alipay_strade_r_usd
FROM 
    (SELECT `load_strade_info`.`Partner_transaction_id` AS `order_id` ,
         sum( `load_strade_info`.`Rmb_amount`) AS `alipay_actual_recieve` ,
         sum(( `load_strade_info`.`Refund` * `load_strade_info`.`Rate`)) AS `refund` ,
         sum(`load_strade_info`.`Amount`) AS `alipay_actual_recieve_usd` ,
         sum(`load_strade_info`.`Refund`) AS `refund_usd` ,
         0 AS `alipay_strade_p` ,
         0 AS `alipay_strade_r` ,
         0 AS `alipay_strade_p_usd` ,
         0 AS `alipay_strade_r_usd`
    FROM `load_strade_info`
    GROUP BY  `load_strade_info`.`Partner_transaction_id`
    UNION
    SELECT `load_strade_info`.`Partner_transaction_id` AS `order_id` ,
         0 AS `alipay_actual_recieve` ,
         0 AS `refund` ,
         0 AS `alipay_actual_recieve_usd` ,
         0 AS `refund_usd` ,
         sum( `load_strade_info`.`Rmb_amount`) AS `alipay_strade_p` ,
         0 AS `alipay_strade_r` ,
         sum(`load_strade_info`.`Amount`) AS `alipay_strade_p_usd` ,
         0 AS `alipay_strade_r_usd`
    FROM `load_strade_info`
    WHERE SUBSTR(Type
    FROM 1 FOR 1) = 'P'
    GROUP BY  `load_strade_info`.`Partner_transaction_id`
    UNION
    SELECT `load_strade_info`.`Partner_transaction_id` AS `order_id` ,
         0 AS `alipay_actual_recieve` ,
         0 AS `refund` ,
         0 AS `alipay_actual_recieve_usd` ,
         0 AS `refund_usd` ,
         0 AS `alipay_strade_p` ,
         sum( `load_strade_info`.`Rmb_amount`) AS `alipay_strade_r` ,
         0 AS `alipay_strade_p_usd` ,
         sum(`load_strade_info`.`Amount`) AS `alipay_strade_r_usd`
    FROM `load_strade_info`
    WHERE SUBSTR(Type
    FROM 1 FOR 1) = 'R'
    GROUP BY  `load_strade_info`.`Partner_transaction_id`) AS t1
GROUP BY  t1.order_id