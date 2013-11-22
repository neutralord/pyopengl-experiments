import sys

try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GL import shaders
    from OpenGL.arrays import vbo
    from vrml.arrays import *
    from numpy import concatenate, identity, transpose, multiply
    from datetime import datetime
except:
    print '''
ERROR: PyOpenGL not installed properly.
        '''
    sys.exit()

class Sample8:
    def __init__(self):
        self.current_time = None
        self.current_angle = 0.0

        glClearColor (0.0, 0.0, 0.0, 0.0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_DEPTH_TEST)

        vertex_shader = shaders.compileShader("""#version 430 core
        in vec4 vPosition;
        in vec4 vColor;
        uniform mat4 modelMatrix;
        uniform float rotationAngle;
        varying vec4 varyingColor;

        // function from http://www.neilmendoza.com/glsl-rotation-about-an-arbitrary-axis/
        mat4 rotationMatrix(vec3 axis, float angle) {
            axis = normalize(axis);
            float s = sin(angle);
            float c = cos(angle);
            float oc = 1.0 - c;

            return mat4(oc * axis.x * axis.x + c,           oc * axis.x * axis.y - axis.z * s,  oc * axis.z * axis.x + axis.y * s,  0.0,
                        oc * axis.x * axis.y + axis.z * s,  oc * axis.y * axis.y + c,           oc * axis.y * axis.z - axis.x * s,  0.0,
                        oc * axis.z * axis.x - axis.y * s,  oc * axis.y * axis.z + axis.x * s,  oc * axis.z * axis.z + c,           0.0,
                        0.0,                                0.0,                                0.0,                                1.0);
        }

        void main() {
            mat4 rotation = rotationMatrix(vec3(0.1, 0.2, 0.3), rotationAngle);
            gl_Position = modelMatrix * rotation * vPosition;
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
        self.rotation_angle_location = glGetUniformLocation(
            self.shader, 'rotationAngle'
        )

        vertex_positions = array([
            -1.0, -1.0, -1.0, 1.0,
            -1.0, -1.0, 1.0, 1.0,
            -1.0, 1.0, -1.0, 1.0,
            -1.0, 1.0, 1.0, 1.0,
            1.0, -1.0, -1.0, 1.0,
            1.0, -1.0, 1.0, 1.0,
            1.0, 1.0, -1.0, 1.0,
            1.0, 1.0, 1.0, 1.0
        ], 'f')

        vertex_colors = array([
            1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 0.0, 1.0,
            1.0, 0.0, 1.0, 1.0,
            1.0, 0.0, 0.0, 1.0,
            0.0, 1.0, 1.0, 1.0,
            0.0, 1.0, 0.0, 1.0,
            0.0, 0.0, 1.0, 1.0,
            0.5, 0.5, 0.5, 1.0
        ], 'f')

        self.vertex_buffer_object = vbo.VBO(concatenate((vertex_positions, vertex_colors)))
        self.vertex_buffer_object.bind()

        self.vertex_indices = vbo.VBO(
            array([
                0, 1, 2, 3, 6, 7, 4, 5,
                0xFFFF,
                2, 6, 0, 4, 1, 5, 3, 7
            ], 'I'),
            target=GL_ELEMENT_ARRAY_BUFFER)
        self.vertex_indices.bind()

        glEnable(GL_PRIMITIVE_RESTART)
        glPrimitiveRestartIndex(0xFFFF)

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
        if self.current_time is None:
            self.current_time = datetime.now()
        self.delta_time = datetime.now() - self.current_time
        self.current_time = datetime.now()
        self.current_angle += 0.000002 * self.delta_time.microseconds
        print self.current_angle
        try:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            translation_matrix = identity(4, 'f') # really it scale matrix there
            translation_matrix[-1][-1] = 2
            glUniformMatrix4fv(self.model_matrix_location, 1 , GL_TRUE, translation_matrix.tolist())
            glUniform1f(self.rotation_angle_location, self.current_angle)
            glDrawElements(GL_TRIANGLE_STRIP, 17, GL_UNSIGNED_INT, self.vertex_indices)
        finally:
            glFlush()


if __name__ == '__main__':
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(250, 250)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("sample 8")
    sample = Sample8()
    glutDisplayFunc(sample.display)
    glutIdleFunc(sample.display)
    glutMainLoop()