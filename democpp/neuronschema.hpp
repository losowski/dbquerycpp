#ifndef NEURONSCHEMA_HPP
#define NEURONSCHEMA_HPP
#include "dbconnection.hpp"
#include "dbtransaction.hpp"
#include "tbody.hpp"
#include "tindividual.hpp"
using namespace std;
using namespace dbquery;
namespace neuronSchema
{

typedef map < int , ptbody > maptbody;
typedef map < int , ptindividual > maptindividual;
class neuronSchema : public dbquery::DBConnection
{
	public:
		neuronSchema (const string & connection);
	public:
		~neuronSchema (void);

	public:
		//Get single child objects
		ptbody gettbody(int id, string name);
		ptbody gtbody(int primaryKey);
		ptbody inserttbody(string name);
		paptbody getMultipletbody(string & sqlWhereClause);
		ptindividual gettindividual(int body_id, int id, string name);
		ptindividual gtindividual(int primaryKey);
		ptindividual inserttindividual(int body_id, string name);
		paptindividual getMultipletindividual(string & sqlWhereClause);
	private:
		maptbody					tbodyMap;
		maptindividual					tindividualMap;
};


}
#endif //NEURONSCHEMA_HPP
