using System;
using System.Linq;
using Gibbed.Borderlands2.GameInfo;

namespace Gibbed.Borderlands2.Probe
{
    internal static class Program
    {
        private static void Main()
        {
            InfoManager.Touch();
            var set = InfoManager.AssetLibraryManager.GetSet(0);
            var lib = set.Libraries[AssetGroup.WeaponTypes];
            Console.WriteLine("=== WeaponTypes sublibraries (first 2, first 6 assets each) ===");
            int si = 0;
            foreach (var sub in lib.Sublibraries)
            {
                Console.WriteLine($"sublib[{si}] package={sub.Package} assets={sub.Assets.Count}");
                foreach (var a in sub.Assets.Take(6)) Console.WriteLine("   " + a);
                if (++si >= 2) break;
            }
            var libb = set.Libraries[AssetGroup.BalanceDefs];
            Console.WriteLine("=== WeaponBalance sublibraries (first 2, first 6 assets each) ===");
            si = 0;
            foreach (var sub in libb.Sublibraries)
            {
                Console.WriteLine($"sublib[{si}] package={sub.Package} assets={sub.Assets.Count}");
                foreach (var a in sub.Assets.Take(6)) Console.WriteLine("   " + a);
                if (++si >= 2) break;
            }
        }
    }
}
