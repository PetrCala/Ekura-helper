using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MINER
{
    public class MyProcess
    {
        public string ProcessName {get; set; }
        public int ProcessID {get; set; }

        public MyProcess(string name, int id)
        {
            ProcessName = name;
            ProcessID = id;
        }
    }
}