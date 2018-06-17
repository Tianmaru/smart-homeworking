(define (domain puzzle)
  (:types tile position)

  (:predicates
    (at ?x - tile ?p - position)
    (empty ?p - position)
    (neighbor ?p - position ?q - position)
  )

  (:action move
    :parameters (?x - tile ?f ?t - position)
    :precondition
      (and
        (at ?x ?f)
        (empty ?t)
        (neighbor ?f ?t)
      )
    :effect
      (and
        (at ?x ?t)
        (empty ?f)
      )
  )
)
