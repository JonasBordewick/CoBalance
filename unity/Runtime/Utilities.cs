using System;
using System.Collections.Generic;
using System.IO;
using UnityEngine;

namespace BalancingFramework
{
    public static class Utilities
    {
        public static string Nicify(string fieldName)
        {
            // quick nicify: "baseDamage" -> "Base Damage"
            if (string.IsNullOrWhiteSpace(fieldName)) return fieldName;
            var chars = new List<char>(fieldName.Length * 2);
            chars.Add(char.ToUpper(fieldName[0]));
            for (int i = 1; i < fieldName.Length; i++)
            {
                var c = fieldName[i];
                if (char.IsUpper(c) && fieldName[i - 1] != ' ')
                    chars.Add(' ');
                chars.Add(c);
            }
            return new string(chars.ToArray());
        }

        public static string GetFrameworkFolderPath()
        {
            var projectRoot = Directory.GetParent(Application.dataPath)?.FullName ?? Application.dataPath;
            return System.IO.Path.Combine(projectRoot, "Balancing");
        }

        public static string GetLogFilePath(string logfileName)
        {
            return System.IO.Path.Combine(
                GetFrameworkFolderPath(),
                "Logs",
                logfileName
            );
        }
        
        public static string GetBalanceFilePath(string balanceFileName)
        {
            if (string.IsNullOrEmpty(balanceFileName))
            {
                balanceFileName = "default_balance.json";
            }

            if (balanceFileName.EndsWith(".json"))
            {
                return System.IO.Path.Combine(
                    GetFrameworkFolderPath(),
                    "Balances",
                    balanceFileName
                );
            }
            
            return System.IO.Path.Combine(
                GetFrameworkFolderPath(),
                "Balances",
                balanceFileName + ".json"
            );
            
            
            
        }
        
        public static string GetArg(string name)
        {
            var args = Environment.GetCommandLineArgs();

            for (int i = 0; i < args.Length; i++)
            {
                if (args[i] == name && i + 1 < args.Length)
                    return args[i + 1];
            }

            return null;
        }
        
        public static bool HasArg(string name)
        {
            var args = Environment.GetCommandLineArgs();
            for (int i = 0; i < args.Length; i++)
            {
                if (args[i] == name)
                    return true;
            }
            return false;
        }
        
    }
}