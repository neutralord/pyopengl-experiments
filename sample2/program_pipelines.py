import sys

try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GL import shaders
    from OpenGL.arrays import vbo
    from vrml.arrays import *
    from ctypes import byref
except:
    print '''
ERROR: PyOpenGL not installed properly.
        '''
    sys.exit()

class Sample5:
    def __init__(self):
        glClearColor (0.0, 0.0, 0.0, 0.0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        vertex_shader = shaders.compileShader("""#version 430 core
        layout (location = 0) in vec4 vPosition;

        out gl_PerVertex {
            vec4 gl_Position;
        };

        void main() {
            gl_Position = vPosition;
        }""", GL_VERTEX_SHADER)

        fragment_shader_red = shaders.compileShader("""#version 430 core
        out vec4 fColor;

        void main() {
            fColor = vec4(1.0, 0.0, 0.0, 1.0);
        }""", GL_FRAGMENT_SHADER)

        fragment_shader_green = shaders.compileShader("""#version 430 core
        out vec4 fColor;

        void main() {
            fColor = vec4(0.0, 1.0, 0.0, 1.0);
        }""", GL_FRAGMENT_SHADER)

        self.position_shader = shaders.compileProgram(
            vertex_shader,
            separable=True
        )

        self.red_shader = shaders.compileProgram(
            fragment_shader_red,
            separable=True
        )

        self.green_shader = shaders.compileProgram(
            fragment_shader_green,
            separable=True
        )

        pipeline_red = GLuint()
        glGenProgramPipelines(1, pipeline_red)
        glUseProgramStages(pipeline_red, GL_VERTEX_SHADER_BIT, self.position_shader)
        glUseProgramStages(pipeline_red, GL_FRAGMENT_SHADER_BIT, self.red_shader)

        pipeline_green = GLuint()
        glGenProgramPipelines(1, pipeline_green)
        glUseProgramStages(pipeline_green, GL_VERTEX_SHADER_BIT, self.position_shader)
        glUseProgramStages(pipeline_green, GL_FRAGMENT_SHADER_BIT, self.green_shader)

        glBindProgramPipeline(pipeline_red) # or pipeline_green

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
            0,
            2, GL_FLOAT, False, 0, self.vbo
        )
        glEnableVertexAttribArray(0)

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
    glutCreateWindow("sample 5")
    sample = Sample5()
    glutDisplayFunc(sample.display)
    glutMainLoop()