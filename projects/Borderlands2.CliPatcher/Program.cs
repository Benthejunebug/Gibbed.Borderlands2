/* Headless CLI patcher for Borderlands 2 saves (no WPF / no Windows required).
 * Usage:
 *   bl2-clipatcher <save.sav> [--level N] [--all] [--slot INDEX]
 * Proves the "level 80 weapon on a level 1 character" modification works on Linux.
 */
using System;
using System.Collections.Generic;
using System.IO;
using Gibbed.Borderlands2.FileFormats;
using Gibbed.Borderlands2.FileFormats.Items;
using Gibbed.Borderlands2.GameInfo;
using Gibbed.Borderlands2.ProtoBufFormats.WillowTwoSave;

namespace Gibbed.Borderlands2.CliPatcher
{
    internal static class Program
    {
        private static int Main(string[] args)
        {
            try
            {
                return Run(args);
            }
            catch (Exception e)
            {
                Console.Error.WriteLine("error: " + e.Message);
                return 1;
            }
        }

        private static int Run(string[] args)
        {
            string path = null;
            int level = 80;
            bool all = false;
            int? slot = null;

            for (int i = 0; i < args.Length; i++)
            {
                var a = args[i];
                if (a == "--level" && i + 1 < args.Length) level = int.Parse(args[++i]);
                else if (a == "--all") all = true;
                else if (a == "--slot" && i + 1 < args.Length) slot = int.Parse(args[++i]);
                else if (a.StartsWith("--") == false && path == null) path = a;
                else Console.Error.WriteLine("ignoring unknown arg: " + a);
            }

            if (path == null)
            {
                Console.Error.WriteLine("usage: bl2-clipatcher <save.sav> [--level N] [--all] [--slot INDEX]");
                return 2;
            }
            if (File.Exists(path) == false)
            {
                Console.Error.WriteLine("save not found: " + path);
                return 2;
            }

            SaveFile save;
            using (var input = File.OpenRead(path))
            {
                InfoManager.Touch(); // ensure GameInfo data is loaded for decode
                save = SaveFile.Deserialize(input, Platform.PC, SaveFile.DeserializeSettings.IgnoreReencodeMismatch);
            }

            var sg = save.SaveGame;
            Console.WriteLine($"character level (ExpLevel): {sg.ExpLevel}");
            Console.WriteLine($"backpack weapon slots: {(sg.PackedWeaponData?.Count ?? 0)}");

            int patched = 0;
            if (sg.PackedWeaponData != null)
            {
                for (int i = 0; i < sg.PackedWeaponData.Count; i++)
                {
                    if (slot.HasValue && slot.Value != i) continue;
                    BackpackWeapon weapon;
                    try
                    {
                        weapon = (BackpackWeapon)BackpackDataHelper.Decode(
                            sg.PackedWeaponData[i].InventorySerialNumber, Platform.PC);
                    }
                    catch (Exception e)
                    {
                        Console.WriteLine($"  slot {i}: decode failed ({e.Message})");
                        continue;
                    }

                    if (all || weapon.GameStage != level)
                    {
                        Console.WriteLine($"  slot {i}: GameStage {weapon.GameStage} -> {level}");
                        weapon.GameStage = level;
                        weapon.ManufacturerGradeIndex = Math.Max(weapon.ManufacturerGradeIndex, level);
                        sg.PackedWeaponData[i].InventorySerialNumber =
                            BackpackDataHelper.Encode(weapon, Platform.PC);
                        patched++;
                    }
                    else
                    {
                        Console.WriteLine($"  slot {i}: already {level}, skipped");
                    }
                }
            }

            if (patched == 0)
            {
                Console.WriteLine("nothing to patch.");
                return 0;
            }

            using (var output = File.Create(path + ".patched.sav"))
            {
                save.Serialize(output);
            }

            Console.WriteLine($"patched {patched} weapon(s) -> wrote {path}.patched.sav");
            return 0;
        }
    }
}
