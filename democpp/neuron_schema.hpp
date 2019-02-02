#ifndef NEURON_SCHEMA_HPP
#define NEURON_SCHEMA_HPP

#include <string>
#include <list>
#include <map>
#include <set>
#include <tuple>

#include "tbody.hpp"

using namespace std;

namespace neuronSchema {

class NeuronSchema
{
	public:
		NeuronSchema(void);
		~NeuronSchema(void);
	public:
		void connect(void);
		
	protected:
		tTime									m_lastAccessed; //ctime seconds
		tdbqueryID								m_dbqueryId;
		int										m_mutex;
		tdbqueryList								m_inputdbquerys;					
		tdbqueryList								m_outputdbquerys;
		tTransmitterSensitivity					m_transmitterSensitivity;
		tTransmitterLevel						m_transmitterLevel;
		//Config Items
		tTransmitterID							m_transmitterID;
		tLevel									m_levelToExcitation; // N/1024
		tInterval								m_purgeInterval;  //Seconds
		tCount									m_totalUseCount;
};
}
#endif //NEURON_SCHEMA_HPP
