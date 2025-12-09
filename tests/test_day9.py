import day9
def test_trace():

    p = (2,5)
    q = (7,10)

    assert list(day9.trace_from_corner(p,q)) == [('h',3,5),
                                                 ('h',4,5),
                                                 ('h',5,5),
                                                 ('h',6,5),
                                                 ('h',7,5),
                                                 ('v',2,6),
                                                 ('v',2,7),
                                                 ('v',2,8),
                                                 ('v',2,9),
                                                 ('v',2,10)
                                                 ]

    assert list(day9.trace_from_corner(q,p)) == [('h',6,10),
                                                 ('h',5,10),
                                                 ('h',4,10),
                                                 ('h',3,10),
                                                 ('h',2,10),
                                                 ('v',7,9),
                                                 ('v',7,8),
                                                 ('v',7,7),
                                                 ('v',7,6),
                                                 ('v',7,5)
                                                 ]
    
    p2 = (2,5)
    q2 = (7,3)

    assert list(day9.trace_from_corner(p2,q2)) == [('h',3,5),
                                                 ('h',4,5),
                                                 ('h',5,5),
                                                 ('h',6,5),
                                                 ('h',7,5),
                                                 ('v',2,4),
                                                 ('v',2,3),
                                                 ]

