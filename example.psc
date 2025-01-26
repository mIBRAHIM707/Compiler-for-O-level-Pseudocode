x <- 10
y <- 10 + 20 - 5
IF x > 0 THEN
  z <- 1
ENDIF
IF x = 0 THEN
  z <- 1
ELSE
  z <- 0
ENDIF
FOR i <- 1 TO 5 DO
  x <- x + i
ENDFOR
PRINT x
PROCEDURE add(a, b)
  RETURN a + b
ENDPROCEDURE
x <- add(3, 4)
IF x > 0 THEN
  IF y > 0 THEN
    z <- 1
  ELSE
    z <- 2
  ENDIF
ELSE
  z <- 3
ENDIF
x <- (3 + 2) * (7 - 4)
READ x
PROCEDURE square(n)
  RETURN n * n
ENDPROCEDURE
x <- square(5)
