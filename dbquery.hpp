#ifndef DBQUERY_HPP
#define DBQUERY_HPP

#include <string>
#include <list>
#include <map>
#include <set>
#include <tuple>

using namespace std;

namespace dbquery {

typedef int	tTime;
typedef int	tInterval;

typedef int tdbqueryID;
typedef int tTransmitterID;
typedef int tLevel;
typedef int tCount;

typedef list < tdbqueryID > tdbqueryList;
typedef map < tTransmitterID, int > tTransmitterSensitivity;		 //Transmitter:sensitivity (N/1024)

enum tLevelDataType {
		LEVEL = 1,
		COUNT
	};
typedef map<tTransmitterID, map<tLevelDataType, tuple<tLevel, tCount > > > tTransmitterLevel; //transmitter: {ENUM:(level,count)}:Value

class DBQueryBase
{
	public:
		DBQueryBase(void);
		~DBQueryBase(void);
	public:
		virtual void sync(void) = 0;
		virtual void notify(void) = 0;
		virtual void purgeUnused(void) = 0;
		virtual void preFetch(void) = 0;
		virtual void optimise(void) = 0;
		virtual void generalise(void) = 0;
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
#endif //DBQUERY_HPP
