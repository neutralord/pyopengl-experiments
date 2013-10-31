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
        uniform float end_fog;
        uniform vec4 fog_color;
        void main() {
            float fog; // amount of fog to apply
            float fog_coord; // distance for fog calculation...
            // This function is generally faster and is guaranteed
            // to produce the same result on each run...
            // gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
            gl_Position = ftransform();
            fog_coord = abs(gl_Position.z);
            fog_coord = clamp( fog_coord, 0.0, end_fog);
            fog = (end_fog - fog_coord)/end_fog;
            fog = clamp( fog, 0.0, 1.0);
            gl_FrontColor = mix(fog_color, gl_Color, fog);
        }""", GL_VERTEX_SHADER)

        FRAGMENT_SHADER = shaders.compileShader("""#version 120
        void main() {
            gl_FragColor = gl_Color;
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

        self.UNIFORM_LOCATIONS = {
            'end_fog': glGetUniformLocation( self.shader, 'end_fog' ),
            'fog_color': glGetUniformLocation( self.shader, 'fog_color' ),
        }

    def Render( self, mode = 0):
        """Render the geometry for the scene."""
        BaseContext.Render( self, mode )
        shaders.glUseProgram(self.shader)
        glUniform1f( self.UNIFORM_LOCATIONS['end_fog'],15)
        glUniform4f(self.UNIFORM_LOCATIONS['fog_color'],0,0,0,1)
        glRotate( 45, 0,1,0 )
        glScale( 3,3,3 )
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