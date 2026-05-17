using UnityEngine;
using UnityEngine.Serialization;

namespace BalancingFramework
{
    public sealed class EntityDescriptorComponent : MonoBehaviour, IBalanceableObject
    {
        [SerializeField] private string id;
        [SerializeField] private string displayName;
        [SerializeField] private string category;
        
        EntityDescriptor IBalanceableObject.Descriptor => new EntityDescriptor(
            id: id,
            displayName: string.IsNullOrWhiteSpace(displayName) ? id : displayName,
            category: category ?? ""
        );
    }
    
    public class EntityDescriptor
    {
        public string ID { get; private set; }
        public string DisplayName { get; private set; }
        public string Category { get; private set; }
        public string Description { get; private set; }
        
        public EntityDescriptor(string id, string displayName, string category)
        {
            ID = id;
            DisplayName = displayName;
            Category = category;
        }
    }
}