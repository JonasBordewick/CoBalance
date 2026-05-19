using System;
using System.Collections.Generic;
using UnityEngine;

namespace CoBalance.DTO
{
    [Serializable]
    public class BalanceDTO : IExportableDTO
    {
        public int schemaVersion = 1;
        public List<EntityDTO> entities = new();
        public List<ValuesDTO> values = new();
        
        
        public bool IsValidForExport()
        {
            return true;
        }
    }
    
    [Serializable]
    public class ValuesDTO
    {
        public string id;
        public float value;
    }

    [Serializable]
    public class EntityDTO
    {
        public string entityID;
        public string displayName;
        public string description;
        public List<ParameterDTO> parameters = new();
        public string category = "";
    }
    
    [Serializable]
    public class ParameterDTO
    {
        public string key;
        public string displayName;
        public string type;
        public List<String> tags;
    }
}