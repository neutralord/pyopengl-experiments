from OpenGLContext import testingcontext
BaseContext = testingcontext.getInteractive()
from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGLContext.scenegraph.basenodes import Sphere
from OpenGLContext.arrays import *


class TestContext( BaseContext ):
    def OnInit( self ):
        materialStruct = """
        struct Material {
            vec4 ambient;
            vec4 diffuse;
            vec4 specular;
            float shininess;
        };
        """

        phong_weightCalc = """
        vec2 phong_weightCalc(
            in vec3 light_pos, // light position
            in vec3 half_light, // half-way vector between light and view
            in vec3 frag_normal, // geometry normal
            in float shininess
        ) {
            // returns vec2( ambientMult, diffuseMult )
            float n_dot_pos = max( 0.0, dot(
                frag_normal, light_pos
            ));
            float n_dot_half = 0.0;
            if (n_dot_pos > -.05) {
                n_dot_half = pow(max(0.0,dot(
                    half_light, frag_normal
                )), shininess);
            }
            return vec2( n_dot_pos, n_dot_half);
        }
        """

        vertex = shaders.compileShader(
        """
        attribute vec3 Vertex_position;
        attribute vec3 Vertex_normal;
        varying vec3 baseNormal;
        void main() {
            gl_Position = gl_ModelViewProjectionMatrix * vec4(
                Vertex_position, 1.0
            );
            baseNormal = gl_NormalMatrix * normalize(Vertex_normal);
        }""", GL_VERTEX_SHADER)

        fragment = shaders.compileShader(
            phong_weightCalc + materialStruct + """
        uniform Material material;
        uniform vec4 Global_ambient;
        uniform vec4 lights[ 12 ]; // 3 possible lights 4 vec4's each
        varying vec3 baseNormal;
        void main() {
            vec4 fragColor = Global_ambient * material.ambient;
            int AMBIENT = 0;
            int DIFFUSE = 1;
            int SPECULAR = 2;
            int POSITION = 3;
            int i;
            for (i=0;i<12;i=i+4) {
                // normalized eye-coordinate Light location
                vec3 EC_Light_location = normalize(
                    gl_NormalMatrix * lights[i+POSITION].xyz
                );
                // half-vector calculation
                vec3 Light_half = normalize(
                    EC_Light_location - vec3( 0,0,-1 )
                );
                vec2 weights = phong_weightCalc(
                    EC_Light_location,
                    Light_half,
                    baseNormal,
                    material.shininess
                );
                fragColor = (
                    fragColor
                    + (lights[i+AMBIENT] * material.ambient)
                    + (lights[i+DIFFUSE] * material.diffuse * weights.x)
                    + (lights[i+SPECULAR] * material.specular * weights.y)
                );
            }
            gl_FragColor = fragColor;
        }
        """, GL_FRAGMENT_SHADER)

        self.shader = shaders.compileProgram(vertex,fragment)
        self.coords,self.indices,self.count = Sphere(
            radius = 1
        ).compile()
        self.uniform_locations = {}
        for uniform,value in self.UNIFORM_VALUES:
            location = glGetUniformLocation( self.shader, uniform )
            if location in (None,-1):
                print 'Warning, no uniform: %s'%( uniform )
            self.uniform_locations[uniform] = location

        self.uniform_locations['lights'] = glGetUniformLocation(
            self.shader, 'lights'
        )
        for attribute in (
            'Vertex_position','Vertex_normal',
        ):
            location = glGetAttribLocation( self.shader, attribute )
            if location in (None,-1):
                print 'Warning, no attribute: %s'%( uniform )
            setattr( self, attribute+ '_loc', location )

    UNIFORM_VALUES = [
        ('Global_ambient',(.05,.05,.05,1.0)),
        ('material.ambient',(.2,.2,.2,1.0)),
        ('material.diffuse',(.5,.5,.5,1.0)),
        ('material.specular',(.8,.8,.8,1.0)),
        ('material.shininess',(.995,)),
    ]

    LIGHTS = array([
        x[1] for x in [
            ('lights[0].ambient',(.05,.05,.05,1.0)),
            ('lights[0].diffuse',(.3,.3,.3,1.0)),
            ('lights[0].specular',(1.0,0.0,0.0,1.0)),
            ('lights[0].position',(4.0,2.0,10.0,0.0)),
            ('lights[1].ambient',(.05,.05,.05,1.0)),
            ('lights[1].diffuse',(.3,.3,.3,1.0)),
            ('lights[1].specular',(0.0,1.0,0.0,1.0)),
            ('lights[1].position',(-4.0,2.0,10.0,0.0)),
            ('lights[2].ambient',(.05,.05,.05,1.0)),
            ('lights[2].diffuse',(.3,.3,.3,1.0)),
            ('lights[2].specular',(0.0,0.0,1.0,1.0)),
            ('lights[2].position',(-4.0,2.0,-10.0,0.0)),
        ]
    ], 'f')

    def Render( self, mode = 0):
        """Render the geometry for the scene."""
        BaseContext.Render( self, mode )
        shaders.glUseProgram(self.shader)
        try:
            self.coords.bind()
            self.indices.bind()
            stride = self.coords.data[0].nbytes
            try:
                glUniform4fv(
                    self.uniform_locations['lights'],
                    12,
                    self.LIGHTS
                )
                test_lights = (GLfloat * 12)()
                glGetUniformfv( self.shader, self.uniform_locations['lights'], test_lights )
                print 'Lights', list(test_lights)
                for uniform,value in self.UNIFORM_VALUES:
                    location = self.uniform_locations.get( uniform )
                    if location not in (None,-1):
                        if len(value) == 4:
                            glUniform4f( location, *value )
                        elif len(value) == 3:
                            glUniform3f( location, *value )
                        elif len(value) == 1:
                            glUniform1f( location, *value )
                glEnableVertexAttribArray( self.Vertex_position_loc )
                glEnableVertexAttribArray( self.Vertex_normal_loc )
                glVertexAttribPointer(
                    self.Vertex_position_loc,
                    3, GL_FLOAT,False, stride, self.coords
                )
                glVertexAttribPointer(
                    self.Vertex_normal_loc,
                    3, GL_FLOAT,False, stride, self.coords+(5*4)
                )
                glDrawElements(
                    GL_TRIANGLES, self.count,
                    GL_UNSIGNED_SHORT, self.indices
                )
            finally:
                self.coords.unbind()
                self.indices.unbind()
                glDisableVertexAttribArray( self.Vertex_position_loc )
                glDisableVertexAttribArray( self.Vertex_normal_loc )
        finally:
            shaders.glUseProgram( 0 )

if __name__ == "__main__":
    TestContext.ContextMainLoop()