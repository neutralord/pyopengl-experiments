import sys

try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GL import shaders
    from OpenGL.arrays import vbo
    from vrml.arrays import *
except:
    print '''
ERROR: PyOpenGL not installed properly.
        '''
    sys.exit()

class Sample1:
    def __init__(self):
        glClearColor (0.0, 0.0, 0.0, 0.0)

        vertex_shader = shaders.compileShader("""#version 430 core
        layout (location = 0) in vec4 vPosition;
        void main() {
            gl_Position = vPosition;
        }""", GL_VERTEX_SHADER)

        fragment_shader = shaders.compileShader("""#version 430 core
        out vec4 fColor;
        void main() {
            fColor = vec4(0.0, 0.0, 1.0, 1.0);
        }""", GL_FRAGMENT_SHADER)

        self.shader = shaders.compileProgram(vertex_shader, fragment_shader)
        shaders.glUseProgram(self.shader)

        self.position_location = glGetAttribLocation(
            self.shader, 'vPosition'
        )

        self.vbo = vbo.VBO(
            array([
                [-0.90, -0.90],
                [ 0.85, -0.90],
                [-0.90,  0.85],
                [ 0.90, -0.85],
                [ 0.90,  0.90],
                [-0.85,  0.90],
            ],'f')
        )
        self.vbo.bind()

        glVertexAttribPointer(
            self.position_location,
            2, GL_FLOAT, False, 0, self.vbo
        )
        glEnableVertexAttribArray(self.position_location)

    def display(self):
        try:
            glClear(GL_COLOR_BUFFER_BIT)
            glDrawArrays(GL_TRIANGLES, 0, 6)
        finally:
            glFlush ()


if __name__ == '__main__':
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(250, 250)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("sample 1")
    sample = Sample1()
    glutDisplayFunc(sample.display)
    glutMainLoop()