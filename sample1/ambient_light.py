from OpenGLContext import testingcontext
BaseContext = testingcontext.getInteractive()
from OpenGL.GL import *
from OpenGL.arrays import vbo
from OpenGLContext.arrays import *
from OpenGL.GL import shaders
from OpenGL.GLUT import *
from OpenGLContext.events.timer import Timer


class TestContext( BaseContext ):
    """Creates a simple vertex shader..."""
    def OnInit( self ):
        phong_weightCalc = """
            float phong_weightCalc(
                in vec3 light_pos, // light position
                in vec3 frag_normal // geometry normal
            ) {
                // returns vec2( ambientMult, diffuseMult )
                float n_dot_pos = max( 0.0, dot(
                    frag_normal, light_pos
                ));
                return n_dot_pos;
            }
            """
        vertex = shaders.compileShader( phong_weightCalc +
            """
            uniform vec4 Global_ambient;
            uniform vec4 Light_ambient;
            uniform vec4 Light_diffuse;
            uniform vec3 Light_location;
            uniform vec4 Material_ambient;
            uniform vec4 Material_diffuse;
            attribute vec3 Vertex_position;
            attribute vec3 Vertex_normal;
            varying vec4 baseColor;
            void main() {
                gl_Position = gl_ModelViewProjectionMatrix * vec4(
                    Vertex_position, 1.0
                );
                vec3 EC_Light_location = gl_NormalMatrix * Light_location;
                float diffuse_weight = phong_weightCalc(
                    normalize(EC_Light_location),
                    normalize(gl_NormalMatrix * Vertex_normal)
                );
                baseColor = clamp(
                (
                    // global component
                    (Global_ambient * Material_ambient)
                    // material's interaction with light's contribution
                    // to the ambient lighting...
                    + (Light_ambient * Material_ambient)
                    // material's interaction with the direct light from
                    // the light.
                    + (Light_diffuse * Material_diffuse * diffuse_weight)
                ), 0.0, 1.0);
            }""", GL_VERTEX_SHADER)

        fragment = shaders.compileShader("""
            varying vec4 baseColor;
            void main() {
                gl_FragColor = baseColor;
            }
            """, GL_FRAGMENT_SHADER)

        self.shader = shaders.compileProgram(vertex,fragment)

        self.vbo = vbo.VBO(
            array( [
                [ -1, 0, 0, -1,0,1],
                [  0, 0, 1, -1,0,2],
                [  0, 1, 1, -1,0,2],
                [ -1, 0, 0, -1,0,1],
                [  0, 1, 1, -1,0,2],
                [ -1, 1, 0, -1,0,1],
                [  0, 0, 1, -1,0,2],
                [  1, 0, 1, 1,0,2],
                [  1, 1, 1, 1,0,2],
                [  0, 0, 1, -1,0,2],
                [  1, 1, 1, 1,0,2],
                [  0, 1, 1, -1,0,2],
                [  1, 0, 1, 1,0,2],
                [  2, 0, 0, 1,0,1],
                [  2, 1, 0, 1,0,1],
                [  1, 0, 1, 1,0,2],
                [  2, 1, 0, 1,0,1],
                [  1, 1, 1, 1,0,2],
            ],'f')
        )

        for uniform in (
            'Global_ambient',
            'Light_ambient','Light_diffuse','Light_location',
            'Material_ambient','Material_diffuse',
        ):
            location = glGetUniformLocation( self.shader, uniform )
            if location in (None,-1):
                print 'Warning, no uniform: %s'%( uniform )
            setattr( self, uniform+ '_loc', location )
        for attribute in (
            'Vertex_position','Vertex_normal',
        ):
            location = glGetAttribLocation( self.shader, attribute )
            if location in (None,-1):
                print 'Warning, no attribute: %s'%( uniform )
            setattr( self, attribute+ '_loc', location )

    def Render( self, mode = 0):
        """Render the geometry for the scene."""
        BaseContext.Render( self, mode )
        shaders.glUseProgram(self.shader)
        try:
            self.vbo.bind()
            try:
                glUniform4f( self.Global_ambient_loc, .3,.05,.05,.1 )
                glUniform4f( self.Light_ambient_loc, .2,.2,.2, 1.0 )
                glUniform4f( self.Light_diffuse_loc, 1,1,1,1 )
                glUniform3f( self.Light_location_loc, 2,2,10 )
                glUniform4f( self.Material_ambient_loc, .2,.2,.2, 1.0 )
                glUniform4f( self.Material_diffuse_loc, 1,1,1, 1 )

                glEnableVertexAttribArray( self.Vertex_position_loc )
                glEnableVertexAttribArray( self.Vertex_normal_loc )
                stride = 6*4
                glVertexAttribPointer(
                    self.Vertex_position_loc,
                    3, GL_FLOAT,False, stride, self.vbo
                )
                glVertexAttribPointer(
                    self.Vertex_normal_loc,
                    3, GL_FLOAT,False, stride, self.vbo+12
                )
                glDrawArrays(GL_TRIANGLES, 0, 18)
            finally:
                self.vbo.unbind()
                glDisableVertexAttribArray( self.Vertex_position_loc )
                glDisableVertexAttribArray( self.Vertex_normal_loc )
        finally:
            shaders.glUseProgram( 0 )

if __name__ == "__main__":
    TestContext.ContextMainLoop()