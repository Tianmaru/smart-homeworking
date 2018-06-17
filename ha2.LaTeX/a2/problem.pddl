(define (problem 2puzzle)
  (:domain puzzle)

  (:objects
    t1 t2 t3 - tile
    p11 p12 p21 p22 - position
  )

  (:init
    (neighbor p11 p12)
    (neighbor p11 p21)
    (neighbor p12 p11)
    (neighbor p12 p22)
    (neighbor p21 p11)
    (neighbor p21 p22)
    (neighbor p22 p21)
    (neighbor p22 p12)
    (at t2 p11)
    (at t3 p12)
    (at t1 p22)
    (empty p21)
  )

  (:goal
    (and
      (at t1 p11)
      (at t2 p12)
      (at t3 p21)
    )
  )
)
