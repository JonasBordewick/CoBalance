using System;
using System.Collections.Generic;
using System.Linq;
using CoBalance.Logger;
using UnityEngine.Windows;

namespace CoBalance.DTO
{
    public static class BalanceRepository
    {
        public static void ExportBalanceToFile(string filePath, BalancingAttributeRegistry registry)
        {
            var dto = File.Exists(filePath)
                ? JsonSerializer.ReadJson<BalanceDTO>(filePath)
                : new BalanceDTO();

            var entities = registry.AllEntities;
            var byKey = registry.ByKeySingle;
            
            var existingParameterKeys = dto.values.Select(p => p.id).ToHashSet();

            foreach (var entity in entities)
            {
                if (entity.ID == null)
                    continue;
                
                // if the entity already exists in the DTO, we want to keep its existing parameters and values, so we only create a new EntityDTO if it doesn't exist
                // but maybe we have to update the display name, description or category if they have changed in the meantime, so we update these fields even for existing entities


                var entityDto = dto.entities.FirstOrDefault(e => e.entityID == entity.ID);
                if (entityDto != null)
                {
                    entityDto.displayName = entity.DisplayName;
                    entityDto.description = entity.Description ?? "";
                    entityDto.category = entity.Category ?? "";
                }
                else
                {
                    entityDto = new EntityDTO
                    {
                        entityID = entity.ID,
                        displayName = entity.DisplayName,
                        description = entity.Description ?? "",
                        parameters = new List<ParameterDTO>(),
                        category = entity.Category ?? ""
                    };
                }
                
                var parameters = byKey.Values.Where(p => p.Owner == entity.ID);

                foreach (var param in parameters)
                {
                    if (param.Key == null || existingParameterKeys.Contains(param.Key))
                        continue;

                    var paramDto = new ParameterDTO
                    {
                        key = param.Key,
                        displayName = param.DisplayName,
                        type = ValueTypeToString(param.ValueType),
                        tags = new List<string>()
                    };
                    entityDto.parameters.Add(paramDto);
                    existingParameterKeys.Add(param.Key);

                    dto.values.Add(new ValuesDTO
                    {
                        id = param.Key,
                        value = param.ValueType is ParameterValueType.Float
                            ? Convert.ToSingle(param.GetValue()) 
                            : Convert.ToInt32(param.GetValue())
                    });
                }
                
                if (!dto.entities.Contains(entityDto))
                    dto.entities.Add(entityDto);
            }

            dto = CleanBalanceDTO(dto, registry);
            JsonSerializer.WriteJson(filePath, dto);
        }

        public static void ImportNewFromFile(string filePath)
        {
            var registry = BalancingAttributeRegistry.Instance;
            registry.ClearRegistry();
            registry.RegisterAllEntities();
            
            if (!File.Exists(filePath))
            {
                CoBalanceLogger.LogWarning($"File not found at path: {filePath}. Import aborted.");
                return;
            }
            
            var dto = JsonSerializer.ReadJson<BalanceDTO>(filePath);
            if (dto == null || dto.values == null || dto.entities == null)
            {
                CoBalanceLogger.LogWarning(
                    $"Invalid or empty data in file at path: {filePath}. Import aborted.");
                return;
            }
            
            var appliedCount = 0;
            var skippedMissing = 0;
            var skippedTypeMismatch = 0;
            
            foreach (var valueDto in dto.values)
            {
                if (valueDto == null || string.IsNullOrWhiteSpace(valueDto.id)) 
                    continue;
                
                if (!registry.ByKeyList.TryGetValue(valueDto.id, out var descriptors) || descriptors == null)
                {
                    skippedMissing++;
                    continue;
                }

                foreach (var descriptor in descriptors)
                {
                    bool ok = descriptor.ValueType switch
                    {
                        ParameterValueType.Float => 
                            descriptor.TrySetValueFromObject(valueDto.value),
                        ParameterValueType.Int => 
                            descriptor.TrySetValueFromObject(Convert.ToInt32(valueDto.value)),
                        _ => false
                    };

                    if (ok)
                    {
                        CoBalanceLogger.LogInfo("" +
                                                         $"Applied value for parameter with key: {valueDto.id}. " +
                                                         $"New value: {valueDto.value}");
                        appliedCount++;
                    }
                    else
                    {
                        CoBalanceLogger.LogInfo("" +
                                                         $"Type mismatch when applying value for parameter with key: {valueDto.id}. " +
                                                         $"Expected type: {descriptor.ValueType}, " +
                                                         $"Provided value: {valueDto.value}");
                        skippedTypeMismatch++;
                    }
                }
            }
            CoBalanceLogger.LogInfo($"Balance import completed. Applied values: {appliedCount}, " +
                $"Skipped due to missing parameters: {skippedMissing}, " +
                $"Skipped due to type mismatch: {skippedTypeMismatch}");
        }

        private static BalanceDTO CleanBalanceDTO (BalanceDTO dto, BalancingAttributeRegistry registry)
        {
            var entities = registry.AllEntities;
            
            var deletedEntities = dto.entities.Where(entity => entities.All(e => e.ID != entity.entityID)).ToList();

            foreach (var entity in deletedEntities)
            {
                dto.entities.Remove(entity);
                
                // Remove all parameters belonging to this entity
                var parametersToRemove = dto.values.Where(
                    p => p.id.Contains(entity.entityID)).ToList();
                foreach (var param in parametersToRemove)
                {
                    dto.values.Remove(param);
                }
            }
            
            
            return dto;
        }
        
        private static string ValueTypeToString(ParameterValueType type)
        {
            switch (type)
            {
                case ParameterValueType.Int:
                    return "int";
                case ParameterValueType.Float:
                    return "float";
                default:
                    return "unknown";
            }
        }
    }
}