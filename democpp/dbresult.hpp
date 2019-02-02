#ifndef DBRESULT_HPP
#define DBRESULT_HPP

#include <string>
#include <list>
#include <map>
#include <set>
#include <tuple>

using namespace std;

namespace dbquery {

class DBResult
{
	public:
		DBResult(void);
		DBResult(int primaryKey);
		~DBResult(void);
	public:
		//SELECT
		virtual void getRow(void) = 0;
		//DELETE
		virtual void deleteRow(int primaryKey) = 0;
		//UPDATE
		virtual void saveRow(void) = 0;
		//INSERT
		virtual void addRow(void) = 0;
	protected:
		int			pk;
};


#endif //DBRESULT_HPP
