import sys

try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GL import shaders
    from OpenGL.arrays import vbo
    from vrml.arrays import *
    from numpy import concatenate
    import numpy as np
except:
    print '''
ERROR: PyOpenGL not installed properly.
        '''
    sys.exit()

class Sample10:
    def __init__(self):
        glClearColor (0.0, 0.0, 0.0, 0.0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glClearColor (0.0, 0.0, 0.0, 0.0)

        vertex_shader = shaders.compileShader("""#version 430 core
        in vec4 vPosition;
        in vec4 vColor;
        varying vec4 varyingColor;

        void main() {
            gl_Position = vPosition;
            varyingColor = vColor;
        }""", GL_VERTEX_SHADER)

        fragment_shader = shaders.compileShader("""#version 430 core
        out vec4 fColor;
        varying vec4 varyingColor;

        void main() {
            fColor = varyingColor;
        }""", GL_FRAGMENT_SHADER)

        self.shader = shaders.compileProgram(vertex_shader, fragment_shader)
        shaders.glUseProgram(self.shader)

        self.position_location = glGetAttribLocation(
            self.shader, 'vPosition'
        )
        self.color_location = glGetAttribLocation(
            self.shader, 'vColor'
        )

        vertex_positions = array([
            -1.0, -1.0, 0.0, 1.0,
            1.0, -1.0, 0.0, 1.0,
            -1.0, 1.0, 0.0, 1.0,
            -1.0, -1.0, 0.0, 1.0,
        ], 'f')

        vertex_colors = array([
            255, 255, 255, 255,
            255, 255, 0, 255,
            255, 0, 255, 255,
            0, 255, 255, 255,
        ], 'uint8')

        final_buffer = np.fromstring(vertex_positions.tostring() + vertex_colors.tostring())
        self.vertex_buffer_object = vbo.VBO(final_buffer)
        self.vertex_buffer_object.bind()

        self.vertex_indices = vbo.VBO(array([0, 1, 2], 'I'), target=GL_ELEMENT_ARRAY_BUFFER)
        self.vertex_indices.bind()

        glVertexAttribPointer(
            self.position_location,
            4, GL_FLOAT, False, 0, self.vertex_buffer_object
        )
        glEnableVertexAttribArray(self.position_location)

        glVertexAttribPointer(
            self.color_location,
            4, GL_UNSIGNED_BYTE, True, 0, self.vertex_buffer_object + vertex_positions.nbytes
        )
        glEnableVertexAttribArray(self.color_location)

    def display(self):
        try:
            glClear(GL_COLOR_BUFFER_BIT)
            #glDrawArrays(GL_TRIANGLES, 0, 3)
            glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_INT, self.vertex_indices)
        finally:
            glFlush ()


if __name__ == '__main__':
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(250, 250)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("sample 10")
    sample = Sample10()
    glutDisplayFunc(sample.display)
    glutMainLoop()