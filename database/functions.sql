CREATE OR REPLACE FUNCTION CREATEORDER (
    P_CUSTOMER_ID IN NUMBER,
    P_ORDER_DATE IN VARCHAR2,
    P_STATUS IN VARCHAR2,
    P_TOTAL_AMOUNT IN NUMBER
) RETURN NUMBER IS
    NEW_ID       NUMBER;
    ORDER_EXISTS NUMBER(1, 0);
BEGIN
    INSERT INTO ORDERS (
        CUSTOMER_ID,
        ORDER_DATE,
        STATUS,
        TOTAL_AMOUNT
    ) VALUES (
        P_CUSTOMER_ID,
        TO_DATE(P_ORDER_DATE, 'YYYY-MM-DD'),
        P_STATUS,
        P_TOTAL_AMOUNT
    ) RETURNING ORDER_ID INTO NEW_ID;
    COMMIT;
    RETURN NEW_ID;
END;

