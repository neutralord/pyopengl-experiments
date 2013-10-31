__author__ = 'neutral'

from OpenGLContext import testingcontext
BaseContext = testingcontext.getInteractive()
from OpenGL.GL import *
from OpenGL.arrays import vbo
from OpenGLContext.arrays import *
from OpenGL.GL import shaders
from OpenGL.GLUT import *


class TestContext( BaseContext ):
    """Creates a simple vertex shader..."""
    def OnInit( self ):
        VERTEX_SHADER = shaders.compileShader("""#version 120
        varying vec4 vertex_color;
        void main() {
            gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
            vertex_color = gl_Color;
        }""", GL_VERTEX_SHADER)

        FRAGMENT_SHADER = shaders.compileShader("""#version 120
        varying vec4 vertex_color;
        void main() {
            gl_FragColor = vertex_color;
        }""", GL_FRAGMENT_SHADER)

        self.shader = shaders.compileProgram(VERTEX_SHADER,FRAGMENT_SHADER)

        self.vbo = vbo.VBO(
            array( [
                [  0, 1, 0,  0,1,0 ],
                [ -1,-1, 0,  1,1,0 ],
                [  1,-1, 0,  0,1,1 ],
                [  2,-1, 0,  1,0,0 ],
                [  4,-1, 0,  0,1,0 ],
                [  4, 1, 0,  0,0,1 ],
                [  2,-1, 0,  1,0,0 ],
                [  4, 1, 0,  0,0,1 ],
                [  2, 1, 0,  0,1,1 ],
            ],'f')
        )

    def Render( self, mode):
        """Render the geometry for the scene."""
        BaseContext.Render( self, mode )
        shaders.glUseProgram(self.shader)
        try:
            self.vbo.bind()
            try:
                glEnableClientState(GL_VERTEX_ARRAY);
                glEnableClientState(GL_COLOR_ARRAY);
                glVertexPointer(3, GL_FLOAT, 24, self.vbo )
                glColorPointer(3, GL_FLOAT, 24, self.vbo+12 )
                glDrawArrays(GL_TRIANGLES, 0, 9)
            finally:
                self.vbo.unbind()
                glDisableClientState(GL_VERTEX_ARRAY);
                glDisableClientState(GL_COLOR_ARRAY);
        finally:
            shaders.glUseProgram( 0 )

if __name__ == "__main__":
    TestContext.ContextMainLoop()