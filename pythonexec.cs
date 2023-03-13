using KunyeServis.AxServices.BIKIHSKunyeBilgileriServisiServisGroup;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
//using TinyJson;
using System.IO;
using System.Security.Principal;
using System.CodeDom.Compiler;
using System.Diagnostics;

namespace KunyeServis
{
    internal class Program
    {
        //This place may change
       
        static readonly string confFile = "C:\\Kunye_servis\\KunyeServis\\configuration.json";
        static KunyeConfiguration kc;

        static string urlFile="";
        static string resultFolder = "";
        static string pythonUrl = "";
        static string crawlerPythonCodeUrl = "";
        static string axDomain = "";
        static string axUser = "";
        static string axPassword = ""; 
        static string threadCount = ""; 

        [Serializable]
        public class KunyeConfiguration
        {
            public string urlFile { get; set; }
            public string resultFolder { get; set; }
            public string pythonUrl { get; set; }
            public string crawlerPythonCodeUrl { get; set; }
            public string axDomain { get; set; }
            public string axUser { get; set; }
            public string axPassword { get; set; }
            public string threadCount { get; set; }
           

        }
        

        static void Main(string[] args)
        {

            //Read Json File
            if (File.Exists(confFile))
            {
                string allline1="";
                // Read a text file line by line.
                string[] lines = File.ReadAllLines(confFile);
                //foreach (string line in lines)
                // Console.WriteLine(line);
                foreach (string line in lines)
                {
                    allline1 = allline1 + line;
                }
                kc = JsonConvert.DeserializeObject<KunyeConfiguration>(allline1);


                urlFile = kc.urlFile;
                resultFolder = kc.resultFolder;
                pythonUrl = kc.pythonUrl;
                crawlerPythonCodeUrl = kc.crawlerPythonCodeUrl;
                axDomain = kc.axDomain;
                axUser = kc.axUser;
                axPassword = kc.axPassword;
                threadCount = kc.threadCount; 
                Console.WriteLine("Configuration file found.");

            }
            else
            {
                   urlFile = "C://Kunye_servis//Results//url.txt";
                   resultFolder = "C://Kunye_servis//Results//";
                   pythonUrl = "C://Kunye_servis//Python//python.exe";
                   crawlerPythonCodeUrl = "C://Kunye_servis//Crawler//test.py";
                   axDomain = "";
                   axUser = "";
                   axPassword = "";
                   threadCount = "4"; 

                 try
                {
                    KunyeConfiguration yeniKc = new KunyeConfiguration();
                    yeniKc.urlFile = urlFile;
                    yeniKc.resultFolder = resultFolder;
                    yeniKc.pythonUrl = pythonUrl;
                    yeniKc.crawlerPythonCodeUrl= crawlerPythonCodeUrl;
                    yeniKc.axDomain = axDomain;
                    yeniKc.axUser = axUser;
                    yeniKc.axPassword = axPassword;
                    yeniKc.threadCount = threadCount;

                    var configJson = JsonConvert.SerializeObject(yeniKc);

                    //pass the filepath and filename to the streamwriter constructor
                    StreamWriter swc = new StreamWriter(confFile);
                    //write a line of text
                    swc.WriteLine(configJson);
                    //write a second line of text
                    //close the file
                    swc.Close();
                }
                catch (Exception e)
                {
                    Console.WriteLine("exception: " + e.Message);
                }
                //finally
                {
                    Console.WriteLine("executing finally block.");
                }
                //console.readkey();

                Console.WriteLine("Configuration file NOT found.");
            }

            BIKIHSKunyeBilgileriServisiClient wsClient;
            CallContext context;
                                  
            
            wsClient = new BIKIHSKunyeBilgileriServisiClient();
            wsClient.ClientCredentials.Windows.ClientCredential = new NetworkCredential(axUser, axPassword, axDomain);
            wsClient.InnerChannel.OperationTimeout = new TimeSpan(2, 0, 0);
            context = new CallContext() { Company = "BIK", Language = "en-au" };

            BIKIHSKunyeBilgileriParameters[] yayinListesi = wsClient.getYayinListesi(context);

            


            // ***********************************************************************************************************************

            /*
            var yayinListesi = new List<BIKIHSKunyeBilgileriParameters>
            {
                new BIKIHSKunyeBilgileriParameters
                {       strKunyeAdresiParm = "https://onurerden.com/news/urfanatik.html",
                        strYayinKoduParm = "ZZN00043"

                },
                 new BIKIHSKunyeBilgileriParameters
                {       strKunyeAdresiParm = "https://onurerden.com/news/urfanatik.html",
                        strYayinKoduParm = "ZZN00045"

                },
                  new BIKIHSKunyeBilgileriParameters
                {       strKunyeAdresiParm = "https://onurerden.com/news/urfanatik.html",
                        strYayinKoduParm = "ZZN00046"

                },

            };

            */
            var result2023Json = JsonConvert.SerializeObject(yayinListesi);

            //write json file
            try
            {
               
                //pass the filepath and filename to the streamwriter constructor
                StreamWriter sw = new StreamWriter(urlFile);
                //write a line of text
                sw.WriteLine(result2023Json);
                //write a second line of text
                //close the file
                sw.Close();
            }
            catch (Exception e)
            {
                Console.WriteLine("exception: " + e.Message);
            }
            //finally
            {
                //Console.WriteLine("executing finally block.");
            }
            //console.readkey();



            var processStartInfo = new ProcessStartInfo
            {
                Arguments = crawlerPythonCodeUrl + " " + resultFolder + " "+threadCount,
                FileName = pythonUrl,
                UseShellExecute = false,
                RedirectStandardOutput = true,
                CreateNoWindow = true,
                RedirectStandardError = true,
            };
            var errors = "";
            var results = "";

            Console.WriteLine("Python script will start.\n");
            Console.WriteLine("thread count parameter:" +threadCount +"folder parameter:"+ resultFolder);
            using (var process = Process.Start(processStartInfo))
            {
                //errors = process.StandardError.ReadToEnd();
                results = process.StandardOutput.ReadToEnd();
            }

            //Console.WriteLine("errors:");
            //Console.WriteLine(errors);
            //Console.WriteLine("results");
            //Console.WriteLine(results);



            string allline = "";
            Console.WriteLine("Will Read Crawled Data.");

            //Read Json File
            if (File.Exists(resultFolder + "crawledData.json"))
            {
                Console.WriteLine("Crawled Data file found.");
                // Read a text file line by line.
                string[] lines = File.ReadAllLines(resultFolder + "crawledData.json");
                //foreach (string line in lines)
                // Console.WriteLine(line);
                foreach (string line in lines)
                {
                    allline = allline + line;
                }

            }


            //Deserialize and create Get Object
            // Console.ReadLine();
            BIKIHSKunyeBilgileriParametersGet[] pyResult = JsonConvert.DeserializeObject<BIKIHSKunyeBilgileriParametersGet[]>(allline);
            Console.WriteLine("Successfully parsed Crawled data info");
            var response = wsClient.createUpdateKunyeBilgisi(context, pyResult);
            //foreach (BIKIHSKunyeBilgileriParametersGet z in pyResult)
            //{
            //    Console.WriteLine(z.strYayinKoduParm);

            //    Console.WriteLine(z.strYayinKoduParm + " Kodlu " + response.FirstOrDefault().strServisMesajParm);
            //}


            // Console.ReadKey();
            /*

            foreach (var item in yayinListesi)
            {
                BIKIHSKunyeBilgileriParametersGet[] parmList = new BIKIHSKunyeBilgileriParametersGet[1];
                BIKIHSKunyeBilgileriParametersGet parm = new BIKIHSKunyeBilgileriParametersGet();

                parm.dateKunyeTarihiParm = DateTime.Now;
                parm.strYayinKoduParm = item.strYayinKoduParm;
                parm.strYayinSahibiTicareUnvaniParm = "Yayın sahibi tic";
                parm.strTuzelKisiTemsilcisiParm = "Tüzel kişi temsilcisi";
                parm.strYayinciParm = "Yayinci";
                parm.strSorumluMudurYaziIsleriMuduruParm = "Sorumlu yazı işleri";
                parm.strYonetimYeriParm = "Yönetim yeri";
                parm.strIletisimTelefonuParm = "telefon 054054";
                parm.strKurumsalePostaParm = "yayin@yayin.com";
                parm.strUETSAdresiParm = "yayın uets";
                parm.strYerSaglayiciTicaretUnvaniParm = "yer sağ. tic";
                parm.strYerSaglayiciAdresiParm = "yer sağlayici adres";
                parm.strRawDataXMLParm = "xml__";
                parm.boolKunyeBilgisiTarandiParm = true;

                parmList[0] = parm;
                var response = wsClient.createUpdateKunyeBilgisi(context, parmList);
                Console.WriteLine( parm.strYayinKoduParm + " Kodlu " + response.FirstOrDefault().strServisMesajParm);
            }
            */
            //Console.ReadLine();
            Console.WriteLine("All process completed.");
        }
    }
}
