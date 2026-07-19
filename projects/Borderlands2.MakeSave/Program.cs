/* Creates a synthetic level-1 character with one level-1 weapon, for testing.
 * Mirrors how the real SaveEdit creates a new weapon (only UniqueId + AssetLibrarySetId set;
 * all asset paths default to "None", which Pack() encodes as PackedAssetReference.None). */
using System;
using System.IO;
using Gibbed.Borderlands2.FileFormats;
using Gibbed.Borderlands2.FileFormats.Items;
using Gibbed.Borderlands2.GameInfo;
using Gibbed.Borderlands2.ProtoBufFormats.WillowTwoSave;

namespace Gibbed.Borderlands2.MakeSave
{
    internal static class Program
    {
        private static int Main(string[] args)
        {
            InfoManager.Touch(); // ensure GameInfo data is loaded

            var outPath = args.Length > 0 ? args[0] : "test_save.sav";
            var save = new SaveFile
            {
                Platform = Platform.PC,
                SaveGame = new WillowTwoPlayerSaveGame
                {
                    SaveGameId = 1,
                    ExpLevel = 1,
                    PlayerClass = "GD_Chara_Commando.Character.CharacterClass_Commando",
                    PackedWeaponData = new System.Collections.Generic.List<PackedWeaponData>(),
                },
            };

            var weapon = new BackpackWeapon
            {
                UniqueId = new Random().Next(int.MinValue, int.MaxValue),
                AssetLibrarySetId = 0,
                GameStage = 1,
                ManufacturerGradeIndex = 1,
            };
            save.SaveGame.PackedWeaponData.Add(new PackedWeaponData
            {
                InventorySerialNumber = BackpackDataHelper.Encode(weapon, Platform.PC),
            });

            using (var output = File.Create(outPath))
            {
                save.Serialize(output);
            }
            Console.WriteLine($"wrote test save: {outPath} (char level {save.SaveGame.ExpLevel}, weapon GameStage {weapon.GameStage})");
            return 0;
        }
    }
}
