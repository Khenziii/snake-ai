{
  description = "Snake AI with an CLI";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = {
    self,
    nixpkgs,
    poetry2nix
  }: let
    system = "x86_64-linux";
    pkgs = import nixpkgs { inherit system; };
    inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryApplication;
    inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryPackages;
            
    snake-ai = mkPoetryApplication {
      projectDir = ./.;
    };

    snake-ai-packages = mkPoetryPackages {
      projectDir = ./.;
      groups = [ "dev" ];
    };

    snake-ai-dev-env = pkgs.mkShell {
      name = "dev-shell";
      nativeBuildInputs = [
        pkgs.python310
        snake-ai-packages.poetryPackages
      ];
      shellHook = ''
        export SNAKE_AI_ENV="dev"
      '';
    };
  in {
    packages.${system}.default = snake-ai;
    devShells.${system}.default = snake-ai-dev-env;
  };
}

