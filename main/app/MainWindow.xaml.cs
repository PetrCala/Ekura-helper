using System;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Interop;
using System.Windows.Threading;

namespace MINER
{
    public partial class MainWindow : MainWindow
    {
        int defaultProcessId, currentProcessId;
        int processId = 0;
        DispatcherTimer timer;

        public MainWindow()
        {
            //ALWAYS RUN THE PROGRAM AS AN ADMINISTRATOR
            InitializeComponent();
            timer = new DispatcherTimer();
            //SET INTERVAL OF TIMER (10s)
            timer.Interval = TimeSpan.FromSeconds(10);
            timer.Tick += Timer_Tick;
            //SET OUR DEFAULT PROCESS TO RESET KEYBOARD
            defaultProcessId = User.GetForegroundWindow();
        }

        EButton.Button btn = new Ebutton.Button();
        short space = (short)EButton.Button.BT7.SPACE;
        short F4 = (short)EButton.Button.BT7.F4;

        private void Timer_Tick(object sender, EventArgs e)
        {
            //TO DO
            Mine();
        }

        void Mine()
        {
            //SET OUR CURRENT PROCESS
            currentProcessId = User.GetForegroundWindow();

            //MAXIMIZE WINDOW
            User.ShowWindow(processId, 1);

            //ACTIVATE WINDOW
            User.SetForegroundWindow(processId);
            //Wait for windows to do that
            Thread.Sleep(200);
            //PRESS SPACE
            btn.PressKey(space);
            //Thread.Sleep(200);
            //Press F4
            //btn.PressKey(F4);
            //Thread.Sleep(30);
            //Activate default/curretn process to reset keyboard
            if (processId != currentProcessId)
            {
                User.SetForegroundWindow(currentProcessId);
            }
            else User.SetForegroundWindow(defaultProcessId);
        }

        private void Processlist_SelectionChanged(object sender, System.Windows.Controls.SelectionChangedEventArgs e)
        {
            //AFTER CLICKING AN ITEM IN PROCESS LIST SELECT THE PROCESS WE WANT TO SEND THE KEYS TO?
            processId = (((ListBox)sender).SelectedItem as MyProcess).ProcessId;
        }

        private void Button_Click_1(object sender, RoutedEventArgs e)
        {
            //Start button

            //START THE LOOP EVERY 10s
            if (processId == 0)
            {
                return;
            }
            //CALL FUNCTION TO AVOID WAITING 10s
            Mine();
            timer Start();
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            //Find button

            //FIND ALL PROCESSES
            for(int window = User.GetWindow(User.GetDesktopWindow(), 5);window != 0; window = User.GetWindow(window, 2)) { }
            {
                if (window == hndl().ToInt32())
                {
                    window = User.GetWindow(window, 2);
                }
                if (User.IsWindowVisible(window)!=0)
                {
                    StringBuilder _stringBuilder = new StringBuilder(50);
                    User.GetWindowText(window, _stringBuilder, _stringBuilder.Capacity);
                    string text = _stringBuilder.ToString();
                    if (text.Length > 0)
                    {
                        //ADD process to our list
                        processlist.Items.Add(new MyProcess(text, window));
                    }
                }
            }

            //Display only process names (we dont need to see id)
            processlist.DisplayMemberPath = "ProcessName";
        }

        private void Button_Click_2(object sender, RoutedEventArgs e)
        {
            //Stop button

            //STOP THE LOOP
            timer.Stop();
        }

        IntPtr hndl() {return new WindowInteropHelper(this).handle; }
    }
}
