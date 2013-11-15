import sys

try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GL import shaders
    from OpenGL.arrays import vbo
    from vrml.arrays import *
    from ctypes import c_void_p
except:
    print '''
ERROR: PyOpenGL not installed properly.
        '''
    sys.exit()

class Sample6:
    def __init__(self):
        glClearColor (0.0, 0.0, 0.0, 0.0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glClearColor (0.0, 0.0, 0.0, 0.0)

        vertex_shader = shaders.compileShader("""#version 430 core
        in vec4 vPosition;

        void main() {
            gl_Position = vPosition;
        }""", GL_VERTEX_SHADER)

        fragment_shader = shaders.compileShader("""#version 430 core
        out vec4 fColor;

        void main() {
            fColor = vec4(1.0, 0.0, 0.0, 1.0);
            //fColor = varyingColor;
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
            1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 0.0, 1.0,
            1.0, 0.0, 1.0, 1.0,
            0.0, 1.0, 1.0, 1.0,
        ], 'f')

        vertex_indices = array([0, 1, 2], 'I')

        self.ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,
                vertex_indices.nbytes, vertex_indices, GL_STATIC_DRAW)

        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)

        vertex_buffer_object = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
        glBufferData(GL_ARRAY_BUFFER,
                vertex_positions.nbytes,
                vertex_positions, GL_STATIC_DRAW)

        glVertexAttribPointer(
            self.position_location,
            4, GL_FLOAT, False, 0, c_void_p(0)
        )
        glEnableVertexAttribArray(self.position_location)

    def display(self):
        try:
            glClear(GL_COLOR_BUFFER_BIT)
            glDrawArrays(GL_TRIANGLES, 0, 3)
        finally:
            glFlush ()


if __name__ == '__main__':
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(250, 250)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("sample 6")
    sample = Sample6()
    glutDisplayFunc(sample.display)
    glutMainLoop()