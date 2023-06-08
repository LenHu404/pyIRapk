using System;
using System.Text;
using System.Collections;
using System.IO.Ports;
using System.Net;
using System.Net.Sockets;
using System.Threading;

namespace X6Motion
{
    public class MainMotion
    {
        private ArrayList IncommingNews = new ArrayList();
        private ArrayList Faultys = new ArrayList();
        private ArrayList MySerialPorts = new ArrayList();
        private string MyEndPoint;
        private string MySelfPoint;
        private string anyIPChoosed;
        private int MyLocalPort;
        private string MyIncommingByte;
        private string MyFaultys;
        private string MyComPort;
        private string existingSerialPort;
        private static SerialPort _serialPort;

        public int GetIncommingDataCount
        {
            get
            {
                return this.IncommingNews.Count;
            }
        }

        public int GetFaultysCount
        {
            get
            {
                return this.Faultys.Count;
            }
        }

        public string GetFaultyError
        {
            get
            {
                return this.MyFaultys;
            }
        }

        public string GetIncommingNews
        {
            get
            {
                return this.MyIncommingByte;
            }
        }

        public int GetMyExistingSerialPortsCount
        {
            get
            {
                return this.MySerialPorts.Count;
            }
        }

        public string GetSerialName
        {
            get
            {
                return this.existingSerialPort;
            }
        }

        public string SetComPort
        {
            set
            {
                this.MyComPort = value;
            }
        }

        public void EndPoint(string EndPoint)
        {
            this.MyEndPoint = EndPoint;
        }

        public void SelfPoint(string SelfPoint)
        {
            this.MySelfPoint = SelfPoint;
        }

        public void IPListening(string IpListening)
        {
            this.anyIPChoosed = IpListening;
        }

        public void localPort(int yourLocalPort)
        {
            this.MyLocalPort = yourLocalPort;
        }

        public void IncommingNewsWithNetwork()
        {
            new Thread(new ThreadStart(this.ReceiveDataFromNetwork))
            {
                IsBackground = true
            }.Start();
        }

        private void ReceiveDataFromNetwork()
        {
            UdpClient udpClient = new UdpClient(this.MyLocalPort);
            while (true)
            {
                try
                {
                    IPEndPoint remoteEP = new IPEndPoint(IPAddress.Any, this.MyLocalPort);
                    this.IncommingNews.Add((object)Encoding.UTF8.GetString(udpClient.Receive(ref remoteEP)));
                }
                catch (Exception ex)
                {
                    this.Faultys.Add((object)ex);
                }
            }
        }

        public void ReceiveIncommingNews(int i)
        {
            this.MyIncommingByte = Convert.ToString(this.IncommingNews[i]);
        }

        public void SetIncommingNews(int i, string data)
        {
            this.IncommingNews[i] = (object)data;
        }

        public void ClearIncommingNews()
        {
            this.IncommingNews.Clear();
        }

        public void ReceiveFaultysNews(int i)
        {
            this.MyFaultys = Convert.ToString(this.Faultys[i]);
        }

        public void ClearFaultys()
        {
            this.Faultys.Clear();
        }

        public void SendData(string PitchAxis, string RollAxis, string HeaveAxis, string YawAxis, string LateralAxis, string LongAxis, int port)
        {
            IPEndPoint endPoint = new IPEndPoint(IPAddress.Parse(this.MyEndPoint), port);
            UdpClient udpClient = new UdpClient();
            string str = ":";
            if (PitchAxis.Length == 4)
            {
                if (RollAxis.Length == 4)
                {
                    if (HeaveAxis.Length == 4)
                    {
                        if (YawAxis.Length == 4)
                        {
                            if (LateralAxis.Length == 4)
                            {
                                if (LongAxis.Length == 4)
                                {
                                    try
                                    {
                                        string s = "d" + PitchAxis + str + RollAxis + str + HeaveAxis + str + YawAxis + str + LateralAxis + str + LongAxis + "e";
                                        if (s != "")
                                        {
                                            byte[] bytes = Encoding.UTF8.GetBytes(s);
                                            udpClient.Send(bytes, bytes.Length, endPoint);
                                        }
                                        else if (this.IncommingNews.Count > 0)
                                        {
                                            byte[] bytes = Encoding.UTF8.GetBytes(Convert.ToString(this.IncommingNews[0]));
                                            udpClient.Send(bytes, bytes.Length, endPoint);
                                        }
                                    }
                                    catch (Exception ex)
                                    {
                                        this.Faultys.Add((object)ex);
                                    }
                                }
                                else
                                    this.Faultys.Add((object)"Longaxis.text is too long or too short");
                            }
                            else
                                this.Faultys.Add((object)"Lateralaxis.text is too long or too short");
                        }
                        else
                            this.Faultys.Add((object)"Yawaxis.text is too long or too short");
                    }
                    else
                        this.Faultys.Add((object)"Heaveaxis.text is too long or too short");
                }
                else
                    this.Faultys.Add((object)"Rollaxis.text is too long or too short");
            }
            else
                this.Faultys.Add((object)"Pitchaxis.text is too long or too short");
        }

        public void GetExistingSerialPorts()
        {
            this.MySerialPorts.Clear();
            foreach (object obj in SerialPort.GetPortNames())
                this.MySerialPorts.Add(obj);
        }

        public void GetExistingSerialNames(int i)
        {
            this.existingSerialPort = Convert.ToString(this.MySerialPorts[i]);
        }

        public void InitializeSerialPort(string SerialPortName, int SerialTimeOut)
        {
            MainMotion._serialPort = new SerialPort(SerialPortName, 59999, Parity.None, 8, StopBits.One);
            MainMotion._serialPort.WriteTimeout = SerialTimeOut;
            MainMotion._serialPort.Open();
        }

        public void SendDataWithSerialPort(string PitchAxis, string RollAxis, string HeaveAxis, string YawAxis, string LateralAxis, string LongAxis, int port)
        {
            string str = ":";
            if (PitchAxis.Length == 4)
            {
                if (RollAxis.Length == 4)
                {
                    if (HeaveAxis.Length == 4)
                    {
                        if (YawAxis.Length == 4)
                        {
                            if (LateralAxis.Length == 4)
                            {
                                if (LongAxis.Length == 4)
                                {
                                    try
                                    {
                                        string text = "d" + PitchAxis + str + RollAxis + str + HeaveAxis + str + YawAxis + str + LateralAxis + str + LongAxis + "e";
                                        if (!(text != ""))
                                            return;
                                        MainMotion._serialPort.Write(text);
                                    }
                                    catch (Exception ex)
                                    {
                                        this.Faultys.Add((object)ex);
                                    }
                                }
                                else
                                    this.Faultys.Add((object)"Longaxis.text is too long or too short");
                            }
                            else
                                this.Faultys.Add((object)"Lateralaxis.text is too long or too short");
                        }
                        else
                            this.Faultys.Add((object)"Yawaxis.text is too long or too short");
                    }
                    else
                        this.Faultys.Add((object)"Heaveaxis.text is too long or too short");
                }
                else
                    this.Faultys.Add((object)"Rollaxis.text is too long or too short");
            }
            else
                this.Faultys.Add((object)"Pitchaxis.text is too long or too short");
        }
    }
}
