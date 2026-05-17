using System.IO;
using BalancingFramework.DTO;
using BalancingFramework.Logger;
using UnityEngine;

namespace BalancingFramework
{
    public static class JsonSerializer
    {
        public static void WriteJson(string path, IExportableDTO fileDto)
        {
            if (!fileDto.IsValidForExport())
            {
                BalancingFrameworkLogger.LogWarning("Export produced 0 parameters. Skipping write to avoid overwriting a valid file.");
                return;
            }
            var dir = Path.GetDirectoryName(path);
            if (!string.IsNullOrEmpty(dir))
                Directory.CreateDirectory(dir);

            var json = JsonUtility.ToJson(fileDto, prettyPrint: true);
            File.WriteAllText(path, json);
        }
        
        public static T ReadJson<T>(string path) where T : IExportableDTO
        {
            if (!File.Exists(path))
            {
                throw new FileNotFoundException($"File not found at path: {path}");
            }
            
            var json = File.ReadAllText(path);
            var dto = JsonUtility.FromJson<T>(json);

            if (dto == null)
            {
                throw new InvalidDataException($"Could not deserialize JSON from {path} into type {typeof(T).Name}");
            }
            
            if (!dto.IsValidForExport())
            {
                throw new InvalidDataException($"Deserialized data from {path} is not valid for export.");
            }
            
            return dto;
        }
    }
}