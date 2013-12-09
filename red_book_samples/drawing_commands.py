import sys

try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GL import shaders
    from OpenGL.arrays import vbo
    from vrml.arrays import *
    from numpy import concatenate, identity, transpose, multiply
except:
    print '''
ERROR: PyOpenGL not installed properly.
        '''
    sys.exit()

class Sample7:
    def __init__(self):
        glClearColor (0.0, 0.0, 0.0, 0.0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor (0.0, 0.0, 0.0, 0.0)

        vertex_shader = shaders.compileShader("""#version 430 core
        in vec4 vPosition;
        in vec4 vColor;
        uniform mat4 modelMatrix;
        varying vec4 varyingColor;

        void main() {
            gl_Position = modelMatrix * vPosition;
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
        self.model_matrix_location = glGetUniformLocation(
            self.shader, 'modelMatrix'
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

        self.vertex_buffer_object = vbo.VBO(concatenate((vertex_positions, vertex_colors)))
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
            4, GL_FLOAT, False, 0, self.vertex_buffer_object + vertex_positions.nbytes
        )
        glEnableVertexAttribArray(self.color_location)

    def display(self):
        try:
            glClear(GL_COLOR_BUFFER_BIT)

            translation_matrix = multiply(identity(4, 'f'), 0.25) # it will be scaling matrix also
            translation_matrix[-1][-1] = 1

            translation_matrix[-1][:3] = [-.5, 0., 0.]
            glUniformMatrix4fv(self.model_matrix_location, 1 , GL_FALSE, translation_matrix.tolist())
            glDrawArrays(GL_TRIANGLES, 0, 3)

            translation_matrix[-1][:3] = [0., 0., 0.]
            glUniformMatrix4fv(self.model_matrix_location, 1 , GL_FALSE, translation_matrix.tolist())
            glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_INT, self.vertex_indices)

            translation_matrix[-1][:3] = [.5, 0., 0.]
            glUniformMatrix4fv(self.model_matrix_location, 1 , GL_FALSE, translation_matrix.tolist())
            glDrawElementsBaseVertex(GL_TRIANGLES, 3, GL_UNSIGNED_INT, self.vertex_indices, 1)

            translation_matrix[-1][:3] = [1., 0., 0.]
            glUniformMatrix4fv(self.model_matrix_location, 1 , GL_FALSE, translation_matrix.tolist())
            glDrawArraysInstanced(GL_TRIANGLES, 0, 3, 1)
        finally:
            glFlush ()
            glutPostRedisplay()


if __name__ == '__main__':
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(250, 250)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("sample 7")
    sample = Sample7()
    glutDisplayFunc(sample.display)
    glutMainLoop()