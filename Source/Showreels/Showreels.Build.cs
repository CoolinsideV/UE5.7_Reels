// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;

public class Showreels : ModuleRules
{
	public Showreels(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(new string[] {
			"Core",
			"CoreUObject",
			"Engine",
			"InputCore",
			"EnhancedInput",
			"AIModule",
			"StateTreeModule",
			"GameplayStateTreeModule",
			"UMG",
			"Slate"
		});

		PrivateDependencyModuleNames.AddRange(new string[] { });

		PublicIncludePaths.AddRange(new string[] {
			"Showreels",
			"Showreels/Variant_Platforming",
			"Showreels/Variant_Platforming/Animation",
			"Showreels/Variant_Combat",
			"Showreels/Variant_Combat/AI",
			"Showreels/Variant_Combat/Animation",
			"Showreels/Variant_Combat/Gameplay",
			"Showreels/Variant_Combat/Interfaces",
			"Showreels/Variant_Combat/UI",
			"Showreels/Variant_SideScrolling",
			"Showreels/Variant_SideScrolling/AI",
			"Showreels/Variant_SideScrolling/Gameplay",
			"Showreels/Variant_SideScrolling/Interfaces",
			"Showreels/Variant_SideScrolling/UI"
		});

		// Uncomment if you are using Slate UI
		// PrivateDependencyModuleNames.AddRange(new string[] { "Slate", "SlateCore" });

		// Uncomment if you are using online features
		// PrivateDependencyModuleNames.Add("OnlineSubsystem");

		// To include OnlineSubsystemSteam, add it to the plugins section in your uproject file with the Enabled attribute set to true
	}
}
