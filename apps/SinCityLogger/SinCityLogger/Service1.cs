using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Linq;
using System.ServiceProcess;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using System.Timers;

namespace SinCityLogger
{
    public partial class Service1 : ServiceBase
    {
        private const string FILE_PATH = @"c:\sincity_logger.txt";
        private Timer timer = new Timer();


        public Service1()
        {
            InitializeComponent();
        }

        protected override void OnStart(string[] args)
        {
            ServiceLogic();
        }

        private void ServiceLogic()
        {
            WriteRowIntoLogFile();
            timer.Interval = 60000;
            timer.Elapsed += (sender, args) =>
            {
                WriteRowIntoLogFile();
            };

            timer.Start();
        }

        private void WriteRowIntoLogFile()
        {
            var logFileStream = File.AppendText(FILE_PATH);
            var logEntry = String.Format("{0}: Honey moon service log", DateTime.Now.ToString());
            logFileStream.WriteLine(logEntry);
            logFileStream.Close();
        }

        protected override void OnStop()
        {
            timer.Stop();
        }
    }
}
