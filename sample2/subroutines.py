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

class Sample4:
    def __init__(self):
        glClearColor (0.0, 0.0, 0.0, 0.0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        vertex_shader = shaders.compileShader("""#version 430 core
        layout (location = 0) in vec4 vPosition;
        void main() {
            gl_Position = vPosition;
        }""", GL_VERTEX_SHADER)

        fragment_shader = shaders.compileShader("""#version 430 core
        out vec4 fColor;

        subroutine vec4 ColorFunc(float alpha);
        subroutine (ColorFunc) vec4 redColor(float alpha)
        {
            return vec4(1.0, 0.0, 0.0, alpha);
        }
        subroutine (ColorFunc) vec4 greenColor(float alpha)
        {
            return vec4(0.0, 1.0, 0.0, alpha);
        }
        subroutine uniform ColorFunc getColor;

        subroutine float ChannelFunc();
        subroutine (ChannelFunc) float semiTransparent()
        {
            return 0.5;
        }
        subroutine (ChannelFunc) float opaque()
        {
            return 1.0;
        }
        subroutine uniform ChannelFunc getAlpha;

        void main() {
            fColor = getColor(getAlpha());
        }""", GL_FRAGMENT_SHADER)

        self.shader = shaders.compileProgram(vertex_shader, fragment_shader)
        shaders.glUseProgram(self.shader)

        self.position_location = glGetAttribLocation(
            self.shader, 'vPosition'
        )

        color_function_location = glGetSubroutineUniformLocation(
            self.shader,
            GL_FRAGMENT_SHADER,
            'getColor'
        )

        red_color_index = glGetSubroutineIndex(self.shader, GL_FRAGMENT_SHADER, 'redColor')
        green_color_index = glGetSubroutineIndex(self.shader, GL_FRAGMENT_SHADER, 'greenColor')

        channel_function_location = glGetSubroutineUniformLocation(
            self.shader,
            GL_FRAGMENT_SHADER,
            'getAlpha'
        )

        semi_tranparent_index = glGetSubroutineIndex(self.shader, GL_FRAGMENT_SHADER, 'semiTransparent')
        opaque_index = glGetSubroutineIndex(self.shader, GL_FRAGMENT_SHADER, 'opaque')

        if (red_color_index != GL_INVALID_INDEX and
                    green_color_index != GL_INVALID_INDEX and
                    semi_tranparent_index != GL_INVALID_INDEX and
                    opaque_index != GL_INVALID_INDEX):
            subroutines = {
                channel_function_location: semi_tranparent_index,
                color_function_location: red_color_index,
            }
            subroutine_indices = [None] * (max(subroutines.keys()) + 1)
            for location, index in subroutines.iteritems():
                subroutine_indices[location] = index
            glUniformSubroutinesuiv(GL_FRAGMENT_SHADER, len(subroutine_indices), subroutine_indices)

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
    glutCreateWindow("sample 4")
    sample = Sample4()
    glutDisplayFunc(sample.display)
    glutMainLoop()