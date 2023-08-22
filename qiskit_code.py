from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute
from qiskit.quantum_info import random_statevector, Statevector
from qiskit.visualization import plot_bloch_multivector,plot_bloch_vector
import numpy as np

def Repeater():
    repeater = QuantumCircuit(4)
    # Encoding:
    repeater.h(0)
    repeater.cx(0, 1)
    repeater.h(2)
    repeater.cx(2, 3)
    
    # Repeater:
    repeater.cx(1, 2)
    repeater.h(1)
    
    # BSM:
    repeater.cz(1, 0)
    repeater.cx(2, 3)
    
    # Decoding:
    repeater.cx(0, 3)
    repeater.h(0)
    
    # Gate:
    repeater = repeater.to_gate(label= f'Swapping')
    return repeater

############################
def Teleportation():
    # Entaglment:
    teleportation = QuantumCircuit(4)
    teleportation.h(1)
    teleportation.cx(1,2)

    # Read:
    teleportation.cx(0,1)
    teleportation.h(0)

    # BSM Khald:
    teleportation.cx(1,2)
    teleportation.cz(0,2)
    
    # Gate:
    teleportation = teleportation.to_gate(label= f'Teleportation')
    return teleportation

def Encode(n):
    encode_circuit=QuantumCircuit(n)
    encode_circuit.cx([0,0],[3,6])
    encode_circuit.h([0,3,6])
    
    encode_circuit.cx([0,3,6],[1,4,7])
    encode_circuit.cx([0,3,6],[2,5,8])
    encode_circuit = encode_circuit.to_gate(label= f'Encode')
    return encode_circuit

def CorrectandDecode(n):
    
    #correct
    decode_Circuit=QuantumCircuit(n)
    decode_Circuit.cx([0,3,6],[1,4,7])
    decode_Circuit.cx([0,3,6],[2,5,8])
    decode_Circuit.ccx([2,5,8], [1,4,7], [0,3,6])
    
    
    #Decode
    decode_Circuit.h([0,3,6]) 
    decode_Circuit.cx([0,0],[3,6])
    decode_Circuit.ccx(3, 6, 0)
    
    decode_Circuit = decode_Circuit.to_gate(label= f'Correct and Decode')
    return decode_Circuit

####################################################################
#Bulid Circuit
n=9


qr= QuantumRegister(9,'qr')

qc=QuantumCircuit(qr)

#randomize Qubit 0
S = random_statevector(2)
plot_bloch_multivector(S,title='User State')
qc.initialize(S,0)


encode=Encode(n)
qc.append(encode,range(n))
# job=execute(qc, Aer.get_backend('statevector_simulator'))
# output=job.result().get_statevector()
# plot_bloch_multivector(output,title='After Error corrected')
qc.barrier(label='`noise -->')
qc.x(0)
qc.z(1)
qc.barrier()
#Erro Corriction
decode=CorrectandDecode(n)
qc.append(decode,range(n))
job=execute(qc, Aer.get_backend('statevector_simulator'))
output=job.result().get_statevector()

print('this is the list:',output)
plot_bloch_multivector(output,title='After Error corrected')

qc.barrier()
qc.reset(range(1,4))
repeater1 =Repeater()
qc.append(repeater1,range(0,4))
job=execute(qc, Aer.get_backend('statevector_simulator'))
output=job.result().get_statevector()
plot_bloch_multivector(output,title='After Repeater')


qc.barrier()
qc.reset(range(1,4))
Teleportation1 =Teleportation()
qc.append(Teleportation1,range(0,4))
job=execute(qc, Aer.get_backend('statevector_simulator'))
output=job.result().get_statevector()
plot_bloch_multivector(output,title='After Teleportation')
qc.draw('mpl')
