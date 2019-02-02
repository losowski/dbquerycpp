#include "neuron_schema.hpp"
using namespace std;

namespace neuronSchema {

NeuronSchema::NeuronSchema(string username, string password):
	dbquery::DBConnection(username, password)
{
}

NeuronSchema::~NeuronSchema(void)
{
}


}
