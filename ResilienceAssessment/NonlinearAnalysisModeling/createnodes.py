import openseespy.opensees as ops


def createnodes(a):
    ops.node(a, 12, 13)
    ops.node(a + 1, 13, 23)

