from config import *
import memory

"""
    VertexMenagerie - Gerenciador de Vértices e Texturas

    Esta classe organiza e gerencia dados de vértices de diferentes malhas, facilitando o uso de atlas 
    de texturas (imagem única contendo várias texturas). O objetivo é otimizar o desempenho gráfico 
    reduzindo chamadas à API, agrupando vértices em buffers e carregando-os na GPU. 
    Também gerencia offsets e tamanhos dos vértices, além de mapear e liberar memória da GPU de forma eficiente.
"""
class VertexBufferFinalizationChunk:

    
    def __init__(self):

        self.logical_device = None
        self.physical_device = None
        self.command_buffer = None
        self.queue = None

class VertexMenagerie:

    def __init__(self):

        self.firstIndices = {}
        self.indexCounts = {}
        self.vertexLump = np.array([],dtype=np.float32)
        self.indexLump = []
    
    def consume(self, meshType, vertexData: np.ndarray, indexData: list[int]):

        vertexCount = int(vertexData.size // 7)
        lastVertex = int(self.vertexLump.size // 7)
        indexCount = len(indexData)
        lastIndex = len(self.indexLump)

        self.firstIndices[meshType] = lastIndex
        self.indexCounts[meshType] = indexCount

        self.vertexLump = np.append(self.vertexLump, vertexData)

        for index in indexData:
            self.indexLump.append(index + lastVertex)
    
    def finalize(self, finalization_chunk):

        self.logical_device = finalization_chunk.logical_device

        #criar um buffer de preparação
        input_chunk = memory.BufferInput()
        input_chunk.logical_device = finalization_chunk.logical_device
        input_chunk.physical_device = finalization_chunk.physical_device
        input_chunk.size = self.vertexLump.nbytes
        input_chunk.usage = VK_BUFFER_USAGE_TRANSFER_SRC_BIT
        input_chunk.memory_properties = \
            VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT
        staging_buffer = memory.create_buffer(input_chunk)

        #gravar nele
        memory_location = vkMapMemory(
            device = self.logical_device, memory = staging_buffer.buffer_memory, 
            offset = 0, size = input_chunk.size, flags = 0
        )
        ffi.memmove(memory_location, self.vertexLump, input_chunk.size)
        vkUnmapMemory(device = self.logical_device, memory = staging_buffer.buffer_memory)

        #criar o buffer de vértices
        input_chunk.usage = \
            VK_BUFFER_USAGE_TRANSFER_DST_BIT | VK_BUFFER_USAGE_VERTEX_BUFFER_BIT
        input_chunk.memory_properties = VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT
        self.vertexBuffer = memory.create_buffer(input_chunk)

        #gravar nele a partir do buffer de preparação
        memory.copy_buffer(
            src_buffer = staging_buffer, dst_buffer = self.vertexBuffer,
            size = input_chunk.size, queue = finalization_chunk.queue,
            command_buffer = finalization_chunk.command_buffer
        )

        #destruir o buffer de preparação
        vkDestroyBuffer(
            device = self.logical_device, buffer = staging_buffer.buffer, 
            pAllocator = None
        )
        vkFreeMemory(
            device = self.logical_device, 
            memory = staging_buffer.buffer_memory, pAllocator = None
        )

        self.indexLump = np.array(self.indexLump, dtype=np.uint32)
        #criar um buffer de preparação
        input_chunk.size = self.indexLump.nbytes
        input_chunk.usage = VK_BUFFER_USAGE_TRANSFER_SRC_BIT
        input_chunk.memory_properties = \
            VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT
        staging_buffer = memory.create_buffer(input_chunk)

        #gravar nele
        memory_location = vkMapMemory(
            device = self.logical_device, memory = staging_buffer.buffer_memory, 
            offset = 0, size = input_chunk.size, flags = 0
        )
        ffi.memmove(memory_location, self.indexLump, input_chunk.size)
        vkUnmapMemory(device = self.logical_device, memory = staging_buffer.buffer_memory)

        #criar o buffer de vértices
        input_chunk.usage = \
            VK_BUFFER_USAGE_TRANSFER_DST_BIT | VK_BUFFER_USAGE_INDEX_BUFFER_BIT
        input_chunk.memory_properties = VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT
        self.indexBuffer = memory.create_buffer(input_chunk)

        #gravar nele a partir do buffer de preparação
        memory.copy_buffer(
            src_buffer = staging_buffer, dst_buffer = self.indexBuffer,
            size = input_chunk.size, queue = finalization_chunk.queue,
            command_buffer = finalization_chunk.command_buffer
        )

        #destruir o buffer de preparação
        vkDestroyBuffer(
            device = self.logical_device, buffer = staging_buffer.buffer, 
            pAllocator = None
        )
        vkFreeMemory(
            device = self.logical_device, 
            memory = staging_buffer.buffer_memory, pAllocator = None
        )
    
    def destroy(self):

        vkDestroyBuffer(
            device = self.logical_device, buffer = self.vertexBuffer.buffer, 
            pAllocator = None
        )
        vkFreeMemory(
            device = self.logical_device, 
            memory = self.vertexBuffer.buffer_memory, pAllocator = None
        )

        vkDestroyBuffer(
            device = self.logical_device, buffer = self.indexBuffer.buffer, 
            pAllocator = None
        )
        vkFreeMemory(
            device = self.logical_device, 
            memory = self.indexBuffer.buffer_memory, pAllocator = None
        )