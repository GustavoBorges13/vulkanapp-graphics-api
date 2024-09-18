#version 450

layout(location = 0) out vec3 fragColor;


//triangulo posicao
vec2 positions[3] = vec2[] (
	vec2( 0.0,  -0.5),
	vec2( 0.5,  0.5),
	vec2(-0.5,  0.5)
);

/*
//quadrado posicao
vec2 positions[6] = vec2[] (
    vec2(  0.5,  0.5), // Triângulo 1
    vec2( -0.5,  0.5),
    vec2( -0.5, -0.5),

    vec2(  0.5,  0.5), // Triângulo 2
    vec2( -0.5, -0.5),
    vec2(  0.5, -0.5)
);
*/

//triangulo cores
vec3 colors[3] = vec3[] (
	vec3(1.0, 0.0, 0.0),
	vec3(0.0, 1.0, 0.0),
	vec3(0.0, 0.0, 1.0)
);

/*
//quadrado cores
vec3 colors[6] = vec3[] (
    vec3(1.0, 0.0, 0.0),
    vec3(0.0, 1.0, 0.0),
    vec3(0.0, 0.0, 1.0),

    vec3(1.0, 0.0, 0.0),
    vec3(0.0, 0.0, 1.0),
    vec3(0.0, 1.0, 0.0)
);
*/

void main() {
	gl_Position = vec4(positions[gl_VertexIndex], 0.0, 1.0);
	fragColor = colors[gl_VertexIndex];
}